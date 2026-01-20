# tests/test_timeline_summary_kernel.py

from datetime import datetime, timedelta

from kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from kernel.journals.timeline.timeline_types import TimelineEntryType
from kernel.journals.timeline.timeline_summary import summarize_timeline


def make_entry(ts, t):
    return TimelineEntry(
        entry_id="e",
        created_at=ts,
        type=t,
        title="x",
        description=None,
        action_id=None,
        place_id=None,
        nature=TimelineEntryNature.EVENT,
    )


def test_empty_summary():
    summary = summarize_timeline(entries=[])

    assert summary.total == 0
    assert summary.first_timestamp is None
    assert summary.last_timestamp is None
    assert summary.has_conflicts is False
    assert summary.has_uncertainty is False
    assert summary.has_gaps is False


def test_summary_detects_conflict_and_uncertainty():
    t0 = datetime.utcnow()
    t1 = t0 + timedelta(seconds=1)

    entries = [
        make_entry(t0, TimelineEntryType.ACTION_PROPOSED),
        make_entry(t1, TimelineEntryType.CONFLICT),
    ]

    summary = summarize_timeline(entries=entries)

    assert summary.total == 2
    assert summary.first_timestamp == t0
    assert summary.last_timestamp == t1
    assert summary.has_conflicts is True
