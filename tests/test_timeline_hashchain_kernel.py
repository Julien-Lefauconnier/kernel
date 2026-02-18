# tests/test_timeline_hashchain_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_hashchain import TimelineHashChain


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:03d}",
        created_at=datetime.fromtimestamp(100 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def test_hashchain_is_deterministic():
    entries = [_entry(i) for i in range(5)]
    c1 = TimelineHashChain.build(entries)
    c2 = TimelineHashChain.build(entries)
    assert c1 == c2
    assert c1.head == c2.head


def test_hashchain_detects_tampering():
    entries = [_entry(i) for i in range(5)]
    chain = TimelineHashChain.build(entries)

    tampered = list(entries)
    tampered[3] = TimelineEntry(
        entry_id=tampered[3].entry_id,
        created_at=tampered[3].created_at,
        type=tampered[3].type,
        title="CHANGED",
        description=tampered[3].description,
        action_id=tampered[3].action_id,
        place_id=tampered[3].place_id,
        origin_ref=tampered[3].origin_ref,
        nature=tampered[3].nature,
    )

    with pytest.raises(ValueError):
        chain.verify(tampered)


def test_hashchain_changes_with_order():
    entries = [_entry(i) for i in range(5)]
    c1 = TimelineHashChain.build(entries)
    c2 = TimelineHashChain.build(list(reversed(entries)))
    assert c1.head != c2.head
