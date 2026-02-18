# tests/test_timeline_snapshot_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:04d}",  # >= 8 chars, stable, deterministic
        created_at=datetime.fromtimestamp(100 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )



def test_snapshot_is_deterministic():
    entries = [_entry(i) for i in range(5)]
    s1 = TimelineSnapshot.build(entries)
    s2 = TimelineSnapshot.build(entries)
    assert s1 == s2
    assert s1.head == s2.head


def test_snapshot_detects_tampering():
    entries = [_entry(i) for i in range(5)]
    snapshot = TimelineSnapshot.build(entries)

    tampered = list(entries)
    tampered[2] = _entry(99)

    bad = TimelineSnapshot.build(tampered)

    assert snapshot.head != bad.head


def test_snapshot_verification():
    entries = [_entry(i) for i in range(5)]
    snapshot = TimelineSnapshot.build(entries)
    snapshot.verify()
