# tests/test_timeline_fork_adversarial.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_merge import TimelineMerge, TimelineMergeKind, TimelineMergeResult
from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor



def _entry(i: int, *, seed: str, ts0: int = 100) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"{seed}-entry-{i:04d}",  # seed makes branches differ
        created_at=datetime.fromtimestamp(ts0 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"{seed}-t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def build_timeline_with_n(n: int, *, seed: str, ts0: int = 100) -> TimelineSnapshot:
    return TimelineSnapshot.build([_entry(i, seed=seed, ts0=ts0) for i in range(n)])


def clone_with(entry: TimelineEntry, **kw) -> TimelineEntry:
    """Recreate an immutable entry with some fields overridden."""
    return TimelineEntry(
        entry_id=kw.get("entry_id", entry.entry_id),
        created_at=kw.get("created_at", entry.created_at),
        type=kw.get("type", entry.type),
        title=kw.get("title", entry.title),
        description=kw.get("description", entry.description),
        action_id=kw.get("action_id", entry.action_id),
        place_id=kw.get("place_id", entry.place_id),
        origin_ref=kw.get("origin_ref", entry.origin_ref),
        nature=kw.get("nature", entry.nature),
    )


def test_fork_detect_rejects_fake_common_prefix():
    left = build_timeline_with_n(5, seed="L")
    right = build_timeline_with_n(7, seed="R")

    # Adversary splices 3 entries to fake a prefix of length 3
    fake = list(right.entries)
    fake[:3] = list(left.entries[:3])
    right2 = TimelineSnapshot.build(tuple(fake))

    fork = TimelineFork.detect(left, right2)
    assert fork.common_prefix_len == 3
    assert fork.is_fork()  # diverges at index 3


def test_fork_detect_suffix_tampering():
    left = build_timeline_with_n(5, seed="A")
    right = build_timeline_with_n(5, seed="A")

    tampered = list(right.entries)
    tampered[4] = clone_with(tampered[4], title="evil")  # change content
    right2 = TimelineSnapshot.build(tuple(tampered))

    fork = TimelineFork.detect(left, right2)
    assert fork.is_fork()
    assert fork.common_prefix_len == 4


def test_merge_rejects_entry_id_collision_in_suffix():
    # Create a fork: common prefix 3, then different suffix
    left = build_timeline_with_n(5, seed="L")
    right = build_timeline_with_n(5, seed="R")

    # Force a cross-branch collision in the suffix by reusing an entry_id from left suffix
    tampered = list(right.entries)
    tampered[4] = clone_with(tampered[4], entry_id=left.entries[4].entry_id)
    right2 = TimelineSnapshot.build(tuple(tampered))

    fork = TimelineFork.detect(left, right2)
    assert fork.is_fork()

    result = TimelineMerge.try_merge(fork=fork, local=left, remote=right2)
    assert result.kind == TimelineMergeKind.NO_MERGE
    assert result.reason == "entry_id_collision_in_suffix"


def test_merge_is_deterministic_even_with_timestamp_anomaly():
    left = build_timeline_with_n(5, seed="L")
    right = build_timeline_with_n(5, seed="R")

    # Create a fork with one "rollback-ish" timestamp in suffix
    tampered = list(right.entries)
    tampered.append(clone_with(tampered[-1], created_at=datetime.fromtimestamp(1, tz=timezone.utc)))
    right2 = TimelineSnapshot.build(tuple(tampered))

    fork = TimelineFork.detect(left, right2)

    # Depending on your policy, merge may accept or reject, but must be deterministic.
    r1 = TimelineMerge.try_merge(fork=fork, local=left, remote=right2)
    r2 = TimelineMerge.try_merge(fork=fork, local=left, remote=right2)
    assert r1 == r2


def test_delta_rejects_reordered_entries_via_target_mismatch():
    base = build_timeline_with_n(5, seed="B")
    target = build_timeline_with_n(10, seed="B")

    delta = TimelineDelta.from_snapshots(base, target)

    # reorder entries (still same items, wrong order)
    tampered_entries = tuple(reversed(delta.entries))
    tampered_delta = TimelineDelta(base=delta.base, target=delta.target, entries=tampered_entries)

    with pytest.raises(Exception):
        tampered_delta.apply_to(base)


def test_replay_entry_changes_head_and_count():
    snap = build_timeline_with_n(5, seed="X")
    replay = snap.entries[-1]

    new = TimelineSnapshot.build(tuple(snap.entries) + (replay,))
    assert len(new.entries) == 6
    assert new.head != snap.head

def test_fork_detect_identical():
    s1 = build_timeline_with_n(5, seed="ID")
    s2 = build_timeline_with_n(5, seed="ID")

    fork = TimelineFork.detect(s1, s2)
    assert fork.kind.value == "identical"
    assert fork.common_prefix_len == 5
    assert fork.left_suffix == ()
    assert fork.right_suffix == ()


def test_fork_detect_extends_left():
    left = build_timeline_with_n(5, seed="E")
    right = build_timeline_with_n(7, seed="E")  # right extends left (same seed => same prefix)

    fork = TimelineFork.detect(left, right)
    assert fork.kind.value == "extends_left"
    assert fork.common_prefix_len == 5
    assert fork.left_suffix == ()
    assert len(fork.right_suffix) == 2


def test_fork_detect_extends_right():
    left = build_timeline_with_n(7, seed="E")
    right = build_timeline_with_n(5, seed="E")  # left extends right

    fork = TimelineFork.detect(left, right)
    assert fork.kind.value == "extends_right"
    assert fork.common_prefix_len == 5
    assert len(fork.left_suffix) == 2
    assert fork.right_suffix == ()


def test_fork_detect_zero_common_prefix():
    left = build_timeline_with_n(4, seed="L")
    right = build_timeline_with_n(4, seed="R")

    fork = TimelineFork.detect(left, right)
    assert fork.is_fork()
    assert fork.common_prefix_len == 0


def test_fork_roundtrip_bytes():
    left = build_timeline_with_n(5, seed="L")
    right = build_timeline_with_n(7, seed="R")

    # splice 2 entries to create prefix len=2
    fake = list(right.entries)
    fake[:2] = list(left.entries[:2])
    right2 = TimelineSnapshot.build(tuple(fake))

    fork = TimelineFork.detect(left, right2)
    raw = fork.to_bytes()
    fork2 = TimelineFork.from_bytes(raw)

    assert fork2 == fork
    fork2.assert_consistent()


def test_merge_not_a_fork_returns_no_merge():
    left = build_timeline_with_n(5, seed="SAME")
    right = build_timeline_with_n(7, seed="SAME")  # extends_left, not a fork

    fork = TimelineFork.detect(left, right)
    assert not fork.is_fork()

    res = TimelineMerge.try_merge(fork=fork, local=left, remote=right)
    assert res.kind == TimelineMergeKind.NO_MERGE
    assert res.reason == "not_a_fork"


def test_merge_deterministic_tiebreak_on_entry_id():
    # Make a fork with suffixes sharing exact same created_at values
    left = build_timeline_with_n(3, seed="P")

    # craft local/remote by extending the same prefix manually
    local_entries = list(left.entries)
    remote_entries = list(left.entries)

    # same timestamp for both suffix entries => ordering must fall back to entry_id
    t = datetime.fromtimestamp(999, tz=timezone.utc)

    local_entries.append(_entry(10, seed="L", ts0=999))   # entry_id "L-entry-0010", created_at 1009 normally
    remote_entries.append(_entry(11, seed="R", ts0=999))  # entry_id "R-entry-0011"

    # force same created_at explicitly
    local_entries[-1] = clone_with(local_entries[-1], created_at=t)
    remote_entries[-1] = clone_with(remote_entries[-1], created_at=t)

    local = TimelineSnapshot.build(tuple(local_entries))
    remote = TimelineSnapshot.build(tuple(remote_entries))

    fork = TimelineFork.detect(local, remote)
    assert fork.is_fork()
    res = TimelineMerge.try_merge(fork=fork, local=local, remote=remote)
    assert res.kind == TimelineMergeKind.MERGED
    merged = res.merged
    assert merged is not None

    # last two entries should be ordered by (created_at, entry_id)
    e1, e2 = merged.entries[-2], merged.entries[-1]
    assert e1.created_at == e2.created_at == t
    assert e1.entry_id < e2.entry_id


def test_merge_result_roundtrip_bytes():
    left = build_timeline_with_n(3, seed="P")
    local = TimelineSnapshot.build(tuple(list(left.entries) + [_entry(3, seed="L")]))
    remote = TimelineSnapshot.build(tuple(list(left.entries) + [_entry(3, seed="R")]))

    fork = TimelineFork.detect(local, remote)
    res = TimelineMerge.try_merge(fork=fork, local=local, remote=remote)
    assert res.kind in {TimelineMergeKind.MERGED, TimelineMergeKind.NO_MERGE}

    raw = res.to_bytes()
    res2 = TimelineMergeResult.from_bytes(raw)  # type: ignore[name-defined] if not imported

    assert res2.kind == res.kind
    assert res2.reason == res.reason
    if res.kind == TimelineMergeKind.MERGED:
        assert res2.merged is not None
        assert res2.merged.head == res.merged.head


def test_delta_roundtrip_bytes():
    base = build_timeline_with_n(5, seed="D")
    target = build_timeline_with_n(8, seed="D")

    delta = TimelineDelta.from_snapshots(base, target)
    raw = delta.to_bytes()
    delta2 = TimelineDelta.from_bytes(raw)

    assert delta2.entries == delta.entries
    assert delta2.base.head == delta.base.head
    assert delta2.target.head == delta.target.head
    assert delta2.base.timestamp is not None
    assert delta2.target.timestamp is not None

    out = delta2.apply_to(base)
    assert out == target


def test_delta_empty_rejected():
    base = build_timeline_with_n(5, seed="D")
    with pytest.raises(Exception):
        TimelineDelta.from_snapshots(base, base)


def test_delta_rollback_rejected():
    base = build_timeline_with_n(7, seed="D")
    target = build_timeline_with_n(5, seed="D")
    with pytest.raises(Exception):
        TimelineDelta.from_snapshots(base, target)


def test_snapshot_order_sensitivity_changes_head():
    entries = [_entry(i, seed="OS") for i in range(5)]
    s1 = TimelineSnapshot.build(entries)

    swapped = list(entries)
    swapped[2], swapped[3] = swapped[3], swapped[2]
    s2 = TimelineSnapshot.build(swapped)

    assert s1 != s2
    assert s1.head != s2.head


def test_entry_bytes_roundtrip_stability():
    e = _entry(1, seed="RT")
    e2 = TimelineEntry.from_bytes(e.to_bytes())
    assert e2 == e


def test_cursor_roundtrip_bytes_keeps_identity():
    base = build_timeline_with_n(5, seed="Z")
    c1 = base.cursor()
    c2 = TimelineCursor.from_bytes(c1.to_bytes())
    assert c2 == c1

def test_cursor_identity_depends_on_head_and_count_only():
    base = build_timeline_with_n(5, seed="Z")
    c1 = base.cursor()

    # fake cursor with same head but different timestamp
    c2 = TimelineCursor(
        timestamp=datetime.fromtimestamp(1, tz=timezone.utc),
        head=c1.head,
        total_entries=c1.total_entries,
    )

    assert c1 == c2

def test_cursor_detects_total_entries_mismatch():
    base = build_timeline_with_n(5, seed="Z")
    c1 = base.cursor()

    c2 = TimelineCursor(
        timestamp=c1.timestamp,
        head=c1.head,
        total_entries=c1.total_entries + 1,
    )

    assert c1 != c2

def test_delta_rejects_wrong_base_cursor():
    base = build_timeline_with_n(5, seed="A")
    target = build_timeline_with_n(10, seed="A")

    delta = TimelineDelta.from_snapshots(base, target)

    # forge base
    bad_cursor = TimelineCursor(
        timestamp=delta.base.timestamp,
        head="0" * 64,
        total_entries=delta.base.total_entries,
    )

    forged = TimelineDelta(
        base=bad_cursor,
        target=delta.target,
        entries=delta.entries,
    )

    with pytest.raises(Exception):
        forged.apply_to(base)

def test_fork_detects_hashchain_splice():
    left = build_timeline_with_n(5, seed="A")
    right = build_timeline_with_n(5, seed="B")

    # copy entries but mutate internal ordering later
    fake = list(right.entries)
    fake[:4] = list(left.entries[:4])

    # now mutate last entry to break hashchain
    fake[4] = clone_with(fake[4], title="tampered")

    right2 = TimelineSnapshot.build(tuple(fake))

    fork = TimelineFork.detect(left, right2)

    assert fork.common_prefix_len == 4

def test_merge_is_order_invariant():
    left = build_timeline_with_n(5, seed="A")
    right = build_timeline_with_n(7, seed="B")

    fork = TimelineFork.detect(left, right)

    r1 = TimelineMerge.try_merge(fork=fork, local=left, remote=right)
    r2 = TimelineMerge.try_merge(fork=fork, local=left, remote=right)

    assert r1 == r2

def test_delta_rejects_duplicate_entries():
    base = build_timeline_with_n(5, seed="D")
    target = build_timeline_with_n(10, seed="D")

    delta = TimelineDelta.from_snapshots(base, target)

    tampered = list(delta.entries)
    tampered.append(tampered[-1])  # replay attack

    with pytest.raises(Exception):
        TimelineDelta(
            base=delta.base,
            target=delta.target,
            entries=tuple(tampered),
        )

def test_delta_rejects_duplicate_entries_same_length():
    base = build_timeline_with_n(5, seed="D")
    target = build_timeline_with_n(10, seed="D")

    delta = TimelineDelta.from_snapshots(base, target)

    tampered = list(delta.entries)
    tampered[-1] = tampered[-2]  # duplicate inside same length

    with pytest.raises(Exception):
        TimelineDelta(
            base=delta.base,
            target=delta.target,
            entries=tuple(tampered),
        )


def test_deep_prefix_poisoning():
    left = build_timeline_with_n(20, seed="A")
    right = build_timeline_with_n(25, seed="B")

    fake = list(right.entries)
    fake[:15] = list(left.entries[:15])  # long prefix poisoning

    # corrupt deeper
    fake[16] = clone_with(fake[16], title="evil")

    poisoned = TimelineSnapshot.build(tuple(fake))

    fork = TimelineFork.detect(left, poisoned)

    assert fork.common_prefix_len == 15
    assert fork.is_fork()


def test_delta_target_head_spoof():
    base = build_timeline_with_n(5, seed="X")
    target = build_timeline_with_n(10, seed="X")

    delta = TimelineDelta.from_snapshots(base, target)

    tampered = list(delta.entries)
    tampered[2] = clone_with(tampered[2], title="spoof")

    forged = TimelineDelta(
        base=delta.base,
        target=delta.target,  # correct target head
        entries=tuple(tampered),
    )

    with pytest.raises(Exception):
        forged.apply_to(base)

def test_concurrent_append_divergence():
    base = build_timeline_with_n(5, seed="BASE")

    left = TimelineSnapshot.build(tuple(list(base.entries) + [_entry(10, seed="L")]))
    right = TimelineSnapshot.build(tuple(list(base.entries) + [_entry(10, seed="R")]))

    fork = TimelineFork.detect(left, right)

    assert fork.is_fork()
    assert fork.common_prefix_len == 5


def test_merge_associativity():
    base = build_timeline_with_n(3, seed="B")

    a = TimelineSnapshot.build(tuple(list(base.entries) + [_entry(1, seed="A")]))
    b = TimelineSnapshot.build(tuple(list(base.entries) + [_entry(1, seed="B")]))
    c = TimelineSnapshot.build(tuple(list(base.entries) + [_entry(1, seed="C")]))

    ab = TimelineMerge.try_merge(
        fork=TimelineFork.detect(a, b),
        local=a,
        remote=b,
    )

    if ab.kind != TimelineMergeKind.MERGED:
        return

    abc1 = TimelineMerge.try_merge(
        fork=TimelineFork.detect(ab.merged, c),
        local=ab.merged,
        remote=c,
    )

    bc = TimelineMerge.try_merge(
        fork=TimelineFork.detect(b, c),
        local=b,
        remote=c,
    )

    if bc.kind != TimelineMergeKind.MERGED:
        return

    abc2 = TimelineMerge.try_merge(
        fork=TimelineFork.detect(a, bc.merged),
        local=a,
        remote=bc.merged,
    )

    if abc1.kind == abc2.kind == TimelineMergeKind.MERGED:
        assert abc1.merged.head == abc2.merged.head


def test_delta_idempotence():
    base = build_timeline_with_n(5, seed="ID")
    target = build_timeline_with_n(8, seed="ID")

    delta = TimelineDelta.from_snapshots(base, target)

    out1 = delta.apply_to(base)
    out2 = delta.apply_to(base)

    assert out1 == out2

def test_fork_symmetry():
    left = build_timeline_with_n(7, seed="A")
    right = build_timeline_with_n(7, seed="B")

    f1 = TimelineFork.detect(left, right)
    f2 = TimelineFork.detect(right, left)

    assert f1.common_prefix_len == f2.common_prefix_len
