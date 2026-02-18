# tests/test_timeline_incremental_snapshot_kernel.py

from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry.unsafe(
        entry_id=f"entry-{i:08d}",
        created_at=datetime.fromtimestamp(i, tz=timezone.utc),
        type=None,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
    )


def test_incremental_matches_batch():
    entries = [_entry(i) for i in range(20)]

    batch = TimelineSnapshot.build(entries)

    snap = TimelineSnapshot.build([])
    for e in entries:
        snap = snap.append(e)

    assert snap.head == batch.head


def test_append_is_pure():
    e = _entry(0)

    snap = TimelineSnapshot.build([])

    new_snap = snap.append(e)

    assert snap != new_snap
    assert len(snap.entries) == 0
    assert len(new_snap.entries) == 1


def test_incremental_is_deterministic():
    entries = [_entry(i) for i in range(10)]

    s1 = TimelineSnapshot.build([])
    for e in entries:
        s1 = s1.append(e)

    s2 = TimelineSnapshot.build([])
    for e in entries:
        s2 = s2.append(e)

    assert s1 == s2
