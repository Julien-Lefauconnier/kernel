# tests/test_timeline_invariants_kernel.py

from datetime import datetime, timedelta
import pytest

from kernel.journals.timeline.timeline_entry import TimelineEntry
from kernel.journals.timeline.timeline_types import TimelineEntryType
from kernel.invariants.timeline.timeline_invariants import (
    assert_entry_has_timestamp,
    assert_monotonic,
)


def make_entry(ts: datetime) -> TimelineEntry:
    return TimelineEntry.unsafe(
        entry_id="e1",
        type=next(iter(TimelineEntryType)),
        title="Test",
        description=None,
        action_id=None,
        created_at=ts,
    )


def test_entry_must_have_timestamp():
    entry = make_entry(datetime.utcnow())
    # Should not raise
    assert_entry_has_timestamp(entry)


def test_monotonic_allows_equal_timestamp():
    ts = datetime.utcnow()
    prev = make_entry(ts)
    curr = make_entry(ts)

    # Should not raise
    assert_monotonic(prev, curr)


def test_monotonic_allows_forward_time():
    prev = make_entry(datetime.utcnow())
    curr = make_entry(datetime.utcnow() + timedelta(seconds=1))

    # Should not raise
    assert_monotonic(prev, curr)


def test_monotonic_rejects_backward_time():
    prev = make_entry(datetime.utcnow())
    curr = make_entry(datetime.utcnow() - timedelta(seconds=1))

    with pytest.raises(ValueError):
        assert_monotonic(prev, curr)

