# tests/test_timeline_delta_kernel.py

import pytest
from datetime import datetime, timezone, timedelta

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_delta import (
    TimelineDelta,
    TimelineDeltaBaseMismatch,
    TimelineDeltaTargetMismatch,
    TimelineDeltaEmptyError,
)
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType


# ------------------------------------------------------
# Helpers (aligned with existing kernel tests)
# ------------------------------------------------------

def _entry(i: int) -> TimelineEntry:
    # Align with test_timeline_hashchain_kernel.py style
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
# Core tests
# ------------------------------------------------------

def test_timeline_delta_roundtrip():
    base = _snapshot(5)
    target = _snapshot(10)

    delta = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=target.entries[5:],
    )

    rebuilt = delta.apply_to(base)

    assert rebuilt.cursor() == target.cursor()
    assert rebuilt.entries == target.entries


def test_timeline_delta_size():
    base = _snapshot(3)
    target = _snapshot(7)

    delta = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=target.entries[3:],
    )

    assert delta.size() == 4


def test_timeline_delta_base_mismatch():
    base = _snapshot(5)
    other = _snapshot(4)
    target = _snapshot(10)

    # delta built against "other", applied to "base" => must fail
    delta = TimelineDelta(
        base=other.cursor(),
        target=target.cursor(),
        entries=target.entries[4:],
    )

    with pytest.raises(TimelineDeltaBaseMismatch):
        delta.apply_to(base)


def test_timeline_delta_target_mismatch():
    base = _snapshot(5)
    target = _snapshot(10)

    # attacker modifies target cursor but keeps total_entries consistent
    forged_target = TimelineSnapshot.build(
        list(target.entries[:-1]) + [_entry(999)]
    )

    # same number of entries -> passes structural invariant
    delta = TimelineDelta(
        base=base.cursor(),
        target=forged_target.cursor(),
        entries=target.entries[5:],
    )

    # replay will produce the real target, not forged_target
    with pytest.raises(TimelineDeltaTargetMismatch):
        delta.apply_to(base)




def test_timeline_delta_empty_forbidden():
    snap = _snapshot(5)

    with pytest.raises(TimelineDeltaEmptyError):
        TimelineDelta(
            base=snap.cursor(),
            target=snap.cursor(),
            entries=(),
        )


def test_timeline_delta_monotonicity():
    base = _snapshot(4)
    target = _snapshot(9)

    delta = TimelineDelta(
        base=base.cursor(),
        target=target.cursor(),
        entries=target.entries[4:],
    )

    assert delta.base.total_entries < delta.target.total_entries
    assert delta.base.total_entries + delta.size() == delta.target.total_entries
