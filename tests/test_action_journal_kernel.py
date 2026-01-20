# tests/test_action_journal_kernel.py

from datetime import datetime

import pytest

from kernel.journals.action.action_event import ActionEvent
from kernel.journals.action.action_journal import (
    ActionJournal,
    get_action_journal,
    reset_action_journal,
)


def make_event(
    *,
    event_id: str = "evt-1",
    created_at: datetime | None = None,
    user_ref: str | None = "u1",
    place_ref: str | None = "p1",
    intent: str | None = "remember",
):
    return ActionEvent(
        event_id=event_id,
        created_at=created_at or datetime.utcnow(),
        user_ref=user_ref,
        place_ref=place_ref,
        intent=intent,
    )


# -------------------------------------------------
# Basic behavior
# -------------------------------------------------

def test_action_journal_starts_empty():
    journal = ActionJournal()
    assert journal.list_events() == []


def test_action_journal_appends_event():
    journal = ActionJournal()
    evt = make_event()

    journal.append(evt)

    events = journal.list_events()
    assert len(events) == 1
    assert events[0] is evt


def test_action_journal_is_append_only():
    journal = ActionJournal()
    evt1 = make_event(event_id="e1")
    evt2 = make_event(event_id="e2")

    journal.append(evt1)
    journal.append(evt2)

    events = journal.list_events()
    assert [e.event_id for e in events] == ["e1", "e2"]


def test_action_journal_returns_defensive_copy():
    journal = ActionJournal()
    evt = make_event()

    journal.append(evt)
    events = journal.list_events()
    events.clear()

    # Internal journal must not be affected
    assert len(journal.list_events()) == 1


# -------------------------------------------------
# Singleton behavior
# -------------------------------------------------

def test_global_action_journal_singleton():
    reset_action_journal()

    evt = make_event()
    journal = get_action_journal()

    journal.append(evt)

    events = get_action_journal().list_events()
    assert len(events) == 1
    assert events[0] is evt


def test_reset_action_journal():
    reset_action_journal()
    journal = get_action_journal()

    journal.append(make_event())
    assert len(journal.list_events()) == 1

    reset_action_journal()
    assert journal.list_events() == []
