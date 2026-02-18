# tests/test_timeline_extension_proof_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_extension_proof import TimelineExtensionProof


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


def test_extension_proof_roundtrip():
    base = TimelineSnapshot.build([_entry(i) for i in range(5)])
    target = TimelineSnapshot.build([_entry(i) for i in range(10)])

    proof = TimelineExtensionProof.build(base=base, target=target)

    rebuilt = proof.verify_and_apply(base)

    assert rebuilt.cursor() == target.cursor()


def test_extension_proof_rejects_non_extension():
    base = TimelineSnapshot.build([_entry(i) for i in range(5)])
    other = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999)] + [_entry(6)])

    with pytest.raises(ValueError):
        _ = TimelineExtensionProof.build(base=base, target=other)
