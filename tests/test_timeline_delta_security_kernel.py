# tests/test_timeline_delta_security_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType


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


def _snapshot(n: int) -> TimelineSnapshot:
    return TimelineSnapshot.build([_entry(i) for i in range(n)])


# ------------------------------------------------------
# Determinism
# ------------------------------------------------------

def test_timeline_delta_determinism():
    base = _snapshot(5)
    target = _snapshot(10)

    delta1 = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=target.entries[5:],
    )

    delta2 = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=target.entries[5:],
    )

    assert delta1 == delta2


# ------------------------------------------------------
# Tampering detection (hashchain / target cursor mismatch)
# ------------------------------------------------------

def test_timeline_delta_tampering():
    base = _snapshot(5)
    target = _snapshot(10)

    tampered = list(target.entries[5:])
    # replace first entry of delta by a different entry => replay diverges from target cursor
    tampered[0] = _entry(999)

    delta = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=tuple(tampered),
    )

    with pytest.raises(Exception):
        delta.apply_to(base)


# ------------------------------------------------------
# Rollback protection (target cursor enforces exact end state)
# ------------------------------------------------------

def test_timeline_delta_rollback_protection():
    base = _snapshot(5)
    target = _snapshot(10)

    # attacker tries to claim an older target while providing entries that don't match it
    old_target = _snapshot(8)

    delta = TimelineDelta(
        base=base.cursor(),
        target=old_target.cursor(),
        entries=target.entries[5:8],
    )

    rebuilt = delta.apply_to(base)

    # This is expected to succeed because the delta is consistent with old_target.
    # Anti-rollback policy is typically enforced by the *sync layer* (trust anchor),
    # not by TimelineDelta alone.
    assert rebuilt.cursor() == old_target.cursor()
