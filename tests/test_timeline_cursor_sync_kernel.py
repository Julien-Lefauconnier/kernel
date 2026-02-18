# tests/test_timeline_cursor_sync_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType

def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:08d}",
        created_at=datetime.fromtimestamp(i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )

def test_cursor_empty_is_canonical():
    snap = TimelineSnapshot.build([])
    c = snap.cursor()
    assert c.head is None
    assert c.total_entries == 0

def test_cursor_is_deterministic():
    entries = [_entry(i) for i in range(10)]
    c1 = TimelineSnapshot.build(entries).cursor()
    c2 = TimelineSnapshot.build(entries).cursor()
    assert c1 == c2

def test_cursor_incremental_matches_batch():
    entries = [_entry(i) for i in range(10)]
    batch = TimelineSnapshot.build(entries).cursor()

    snap = TimelineSnapshot.build([])
    for e in entries:
        snap = snap.append(e)
    inc = snap.cursor()

    assert inc == batch
