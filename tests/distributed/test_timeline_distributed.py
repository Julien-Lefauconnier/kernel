# tests/distributed/test_timeline_distributed.py

import random
import pytest
from dataclasses import dataclass
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.timeline.timeline_delta import (
    TimelineDelta,
    TimelineDeltaBaseMismatch,
)
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_merge import (
    TimelineMerge,
    TimelineMergeKind,
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _entry(i: int, *, seed: str, ts0: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"{seed}-entry-{i:06d}",
        created_at=datetime.fromtimestamp(ts0 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"{seed}-t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def build_base(n: int = 5, *, seed: str = "BASE", ts0: int = 10_000) -> TimelineSnapshot:
    return TimelineSnapshot.build([_entry(i, seed=seed, ts0=ts0) for i in range(n)])


def append_n(snap: TimelineSnapshot, n: int, *, seed: str, ts0: int) -> TimelineSnapshot:
    out = snap
    start = len(out.entries)
    for k in range(n):
        out = out.append(_entry(start + k, seed=seed, ts0=ts0))
    return out


# ---------------------------------------------------------------------
# Distributed primitives
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class SyncOutcome:
    kind: str
    a: TimelineSnapshot
    b: TimelineSnapshot


def _try_apply_delta(src: TimelineSnapshot, dst: TimelineSnapshot):
    if src.cursor().total_entries <= dst.cursor().total_entries:
        return None
    try:
        d = TimelineDelta.from_snapshots(dst, src)
        return d.apply_to(dst)
    except Exception:
        return None


def sync_pair(a: TimelineSnapshot, b: TimelineSnapshot) -> SyncOutcome:
    if a.cursor() == b.cursor():
        return SyncOutcome("noop", a, b)

    b2 = _try_apply_delta(a, b)
    if b2 is not None:
        return SyncOutcome("delta_a_to_b", a, b2)

    a2 = _try_apply_delta(b, a)
    if a2 is not None:
        return SyncOutcome("delta_b_to_a", a2, b)

    fork = TimelineFork.detect(a, b)
    if fork.is_fork():
        res = TimelineMerge.try_merge(fork=fork, local=a, remote=b)
        if res.kind == TimelineMergeKind.MERGED:
            return SyncOutcome("merged", res.merged, res.merged)

    return SyncOutcome("no_change", a, b)


def gossip_round(devices, *, rnd: random.Random, steps: int):
    names = list(devices.keys())
    for _ in range(steps):
        i, j = rnd.sample(range(len(names)), 2)
        a, b = names[i], names[j]
        out = sync_pair(devices[a], devices[b])
        devices[a] = out.a
        devices[b] = out.b
    return devices


# ---------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------

def assert_network_valid(devices):
    """
    Minimal invariant:
    every snapshot must be internally buildable and stable.
    """
    for d in devices.values():
        rebuilt = TimelineSnapshot.build(d.entries)
        assert rebuilt.head == d.head
        assert rebuilt.cursor().total_entries == d.cursor().total_entries


def assert_eventual_stability(devices, rnd):
    after = gossip_round(devices.copy(), rnd=rnd, steps=200)
    assert after == devices


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_distributed_eventual_stability_three_devices():
    base = build_base()

    devices = {
        "A": append_n(base, 3, seed="A", ts0=2000),
        "B": append_n(base, 2, seed="B", ts0=3000),
        "C": append_n(base, 4, seed="C", ts0=4000),
    }

    rnd = random.Random(1337)
    devices = gossip_round(devices, rnd=rnd, steps=300)

    assert_network_valid(devices)
    assert_eventual_stability(devices, rnd)


def test_distributed_large_fork_storm_stability():
    base = build_base()

    devices = {}
    for i in range(8):
        devices[f"D{i}"] = append_n(base, 1 + i % 4, seed=f"D{i}", ts0=2000 + 100 * i)

    rnd = random.Random(2026)
    devices = gossip_round(devices, rnd=rnd, steps=1200)

    assert_network_valid(devices)
    assert_eventual_stability(devices, rnd)


def test_network_packet_reordering_safe():
    base = build_base()
    target = append_n(base, 10, seed="A", ts0=2000)

    snaps = [base]
    cur = base
    for _ in range(10):
        cur = cur.append(_entry(len(cur.entries), seed="A", ts0=2000))
        snaps.append(cur)

    deltas = [TimelineDelta.from_snapshots(snaps[i], snaps[i + 1]) for i in range(len(snaps) - 1)]
    packets = [d.to_bytes() for d in deltas]

    rnd = random.Random(99)
    rnd.shuffle(packets)

    recv = base
    for _ in range(20):
        progress = False
        for pkt in list(packets):
            try:
                d = TimelineDelta.from_bytes(pkt)
                recv = d.apply_to(recv)
                packets.remove(pkt)
                progress = True
            except Exception:
                pass
        if not progress:
            break

    assert recv == target


def test_delta_replay_wrong_base():
    base = build_base()
    t1 = append_n(base, 3, seed="A", ts0=2000)
    t2 = append_n(t1, 2, seed="A", ts0=2000)

    d2 = TimelineDelta.from_snapshots(t1, t2)

    with pytest.raises(TimelineDeltaBaseMismatch):
        d2.apply_to(base)


def test_merge_commutativity_when_safe():
    base = build_base()
    a = append_n(base, 3, seed="A", ts0=2000)
    b = append_n(base, 3, seed="B", ts0=3000)

    r1 = TimelineMerge.try_merge(
        fork=TimelineFork.detect(a, b),
        local=a,
        remote=b,
    )

    r2 = TimelineMerge.try_merge(
        fork=TimelineFork.detect(b, a),
        local=b,
        remote=a,
    )

    if r1.kind == r2.kind == TimelineMergeKind.MERGED:
        assert r1.merged.head == r2.merged.head


def test_time_drift_devices_stable():
    base = build_base()

    devices = {
        "A": append_n(base, 3, seed="A", ts0=10_000),
        "B": append_n(base, 3, seed="B", ts0=1),
    }

    rnd = random.Random(7)
    devices = gossip_round(devices, rnd=rnd, steps=200)

    assert_network_valid(devices)


def test_byzantine_coordinated_fork_injection():
    base = build_base()

    # Honest devices
    honest = {
        "H1": append_n(base, 3, seed="H1", ts0=2000),
        "H2": append_n(base, 2, seed="H2", ts0=3000),
    }

    # Malicious cluster coordinating forks
    malicious = {
        "M1": append_n(base, 5, seed="M", ts0=1000),
        "M2": append_n(base, 5, seed="M", ts0=1000),
    }

    devices = {**honest, **malicious}

    rnd = random.Random(42)
    devices = gossip_round(devices, rnd=rnd, steps=500)

    # Honest cluster must remain internally stable
    assert_network_valid({k: devices[k] for k in honest})


def test_network_partition_then_healing():
    base = build_base()

    group_a = {
        "A1": append_n(base, 10, seed="A1", ts0=2000),
        "A2": append_n(base, 8, seed="A2", ts0=2100),
    }

    group_b = {
        "B1": append_n(base, 9, seed="B1", ts0=3000),
        "B2": append_n(base, 7, seed="B2", ts0=3100),
    }

    # partition: gossip inside each group
    rnd = random.Random(123)
    group_a = gossip_round(group_a, rnd=rnd, steps=300)
    group_b = gossip_round(group_b, rnd=rnd, steps=300)

    # heal partition
    devices = {**group_a, **group_b}
    devices = gossip_round(devices, rnd=rnd, steps=600)

    assert_network_valid(devices)


def test_device_churn_stability():
    base = build_base()

    devices = {
        "A": append_n(base, 5, seed="A", ts0=2000),
        "B": append_n(base, 4, seed="B", ts0=3000),
    }

    rnd = random.Random(99)

    # churn simulation
    for _ in range(10):
        devices = gossip_round(devices, rnd=rnd, steps=50)

        # device joins
        devices[f"J{_}"] = append_n(base, 2, seed=f"J{_}", ts0=4000 + _)

        # device leaves
        if len(devices) > 3:
            devices.pop(next(iter(devices)))

    devices = gossip_round(devices, rnd=rnd, steps=200)

    assert_network_valid(devices)
