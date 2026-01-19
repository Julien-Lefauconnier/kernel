# kernel/tests/test_timeline_kernel.py

from datetime import datetime, timedelta

import pytest

from kernel.journals.timeline.timeline_entry import (
    TimelineEntry,
    TimelineEntryNature,
)
from kernel.journals.timeline.timeline_journal import (
    TimelineJournal,
)
from kernel.journals.timeline.timeline_types import (
    TimelineEntryType,
)


def test_timeline_entry_is_immutable():
    """
    Kernel invariant:
    TimelineEntry must be strictly immutable once created.
    """
    entry = TimelineEntry(
        entry_id="evt-1",
        created_at=datetime.utcnow(),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title="Test Event",
        description=None,
        action_id=None,
        place_id=None,
    )

    with pytest.raises(Exception):
        entry.title = "Mutated title"


def test_timeline_journal_append_is_append_only():
    """
    Kernel invariant:
    TimelineJournal must be append-only.
    """
    journal = TimelineJournal()

    t0 = datetime.utcnow()
    t1 = t0 + timedelta(seconds=1)

    entry1 = TimelineEntry(
        entry_id="evt-1",
        created_at=t0,
        type=TimelineEntryType.SYSTEM_NOTICE,
        title="First",
        description=None,
        action_id=None,
        place_id=None,
    )

    entry2 = TimelineEntry(
        entry_id="evt-2",
        created_at=t1,
        type=TimelineEntryType.SYSTEM_NOTICE,
        title="Second",
        description=None,
        action_id=None,
        place_id=None,
    )

    journal.append(entry1)
    journal.append(entry2)

    events = journal.list_events()

    assert len(events) == 2
    assert events[0].entry_id == "evt-1"
    assert events[1].entry_id == "evt-2"


def test_timeline_entry_timestamp_is_canonical():
    """
    Kernel invariant:
    `timestamp` must be a stable alias of `created_at`.
    """
    now = datetime.utcnow()

    entry = TimelineEntry(
        entry_id="evt-ts",
        created_at=now,
        type=TimelineEntryType.SYSTEM_NOTICE,
        title="State snapshot",
        description=None,
        action_id=None,
        place_id=None,
        nature=TimelineEntryNature.STATE,
    )

    assert entry.timestamp is entry.created_at
