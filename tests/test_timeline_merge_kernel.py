# tests/test_timeline_merge_kernel.py

from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_merge import TimelineMerge, TimelineMergeKind


def _entry(i: int, ts: int | None = None, entry_id: str | None = None) -> TimelineEntry:
    t = ts if ts is not None else 100 + i
    eid = entry_id if entry_id is not None else f"entry-{i:03d}"
    return TimelineEntry(
        entry_id=eid,
        created_at=datetime.fromtimestamp(t, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def test_merge_no_merge_when_not_a_fork():
    a = TimelineSnapshot.build([_entry(i) for i in range(5)])
    b = TimelineSnapshot.build([_entry(i) for i in range(8)])

    fork = TimelineFork.detect(a, b)
    r = TimelineMerge.try_merge(fork=fork, local=a, remote=b)

    assert r.kind == TimelineMergeKind.NO_MERGE


def test_merge_interleaves_suffix_deterministically():
    # common prefix of 3 entries: 0,1,2
    prefix = [_entry(0), _entry(1), _entry(2)]

    # left diverges with later timestamps
    left = TimelineSnapshot.build(prefix + [_entry(10, ts=200), _entry(11, ts=210)])

    # right diverges with earlier timestamps
    right = TimelineSnapshot.build(prefix + [_entry(20, ts=150), _entry(21, ts=160)])

    fork = TimelineFork.detect(left, right)
    assert fork.is_fork()

    r = TimelineMerge.try_merge(fork=fork, local=left, remote=right)
    assert r.kind == TimelineMergeKind.MERGED
    assert r.merged is not None

    merged_entries = r.merged.entries

    # prefix unchanged
    assert merged_entries[:3] == tuple(prefix)

    # suffix must be ordered deterministically according to causal order
    suffix = merged_entries[3:]

    expected = sorted(
        suffix,
        key=lambda e: (e.lamport, e.device_id, e.entry_id),
    )

    assert list(suffix) == expected


def test_merge_rejects_entry_id_collision():
    prefix = [_entry(0), _entry(1), _entry(2)]

    left = TimelineSnapshot.build(prefix + [_entry(10, ts=200, entry_id="dup-0001")])
    right = TimelineSnapshot.build(prefix + [_entry(20, ts=150, entry_id="dup-0001")])

    fork = TimelineFork.detect(left, right)
    assert fork.is_fork()

    r = TimelineMerge.try_merge(fork=fork, local=left, remote=right)

    assert r.kind == TimelineMergeKind.NO_MERGE
    assert r.reason == "entry_id_collision_in_suffix"

def test_merge_timestamp_independent():
    prefix = [_entry(0), _entry(1), _entry(2)]

    left = TimelineSnapshot.build(prefix + [_entry(10, ts=10000)])
    right = TimelineSnapshot.build(prefix + [_entry(20, ts=1)])

    fork = TimelineFork.detect(left, right)
    r = TimelineMerge.try_merge(fork=fork, local=left, remote=right)

    suffix = r.merged.entries[3:]
    expected = sorted(
        suffix,
        key=lambda e: (e.lamport, e.device_id, e.entry_id),
    )
    assert list(suffix) == expected
