# tests/test_timeline_commitment_bytes_kernel.py

from datetime import datetime, timezone

import pytest

from veramem_kernel.journals.timeline.timeline_entry import (
    TimelineEntry,
    TimelineEntryNature,
)
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


def test_commitment_bytes_roundtrip():
    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])

    c1 = TimelineCommitment.from_snapshot(snap)
    raw = c1.to_bytes()

    c2 = TimelineCommitment.from_bytes(raw)

    assert c1 == c2


def test_commitment_bytes_deterministic():
    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])

    c1 = TimelineCommitment.from_snapshot(snap)
    c2 = TimelineCommitment.from_snapshot(snap)

    assert c1.to_bytes() == c2.to_bytes()


def test_commitment_bytes_detects_corruption():
    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    raw = bytearray(c.to_bytes())
    raw[-1] ^= 0x01  # flip last bit

    with pytest.raises(Exception):
        TimelineCommitment.from_bytes(bytes(raw))


def test_commitment_bytes_empty_snapshot():
    snap = TimelineSnapshot.build([])

    c = TimelineCommitment.from_snapshot(snap)
    raw = c.to_bytes()

    c2 = TimelineCommitment.from_bytes(raw)

    assert c == c2
