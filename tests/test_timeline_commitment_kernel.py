# tests/test_timeline_commitment_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:05d}",
        created_at=datetime.fromtimestamp(100 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def test_commitment_is_deterministic():
    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])

    c1 = TimelineCommitment.from_snapshot(snap)
    c2 = TimelineCommitment.from_snapshot(snap)

    assert c1 == c2


def test_commitment_detects_tampering():
    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    tampered = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999)])

    with pytest.raises(ValueError):
        c.verify_against(tampered)


def test_commitment_empty_snapshot_is_stable():
    snap = TimelineSnapshot.build([])
    c1 = TimelineCommitment.from_snapshot(snap)
    c2 = TimelineCommitment.from_snapshot(snap)

    assert c1 == c2
