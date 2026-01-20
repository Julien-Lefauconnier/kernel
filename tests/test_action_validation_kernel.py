# tests/test_action_validation_kernel.py

from datetime import datetime

import pytest

from kernel.journals.action.action_validation_event import ActionValidationEvent
from kernel.journals.action.action_validation_journal import (
    ActionValidationJournal,
    get_action_validation_journal,
    reset_action_validation_journal,
)


def make_validation(
    *,
    event_id: str = "v1",
    action_ref: str = "a1",
    decision: str = "ACCEPTED",
    decided_at: datetime | None = None,
):
    return ActionValidationEvent(
        event_id=event_id,
        action_ref=action_ref,
        user_ref="u1",
        place_ref="p1",
        decision=decision,
        decided_at=decided_at or datetime.utcnow(),
    )


# -------------------------------------------------
# Event invariants
# -------------------------------------------------

def test_validation_event_requires_timestamp():
    with pytest.raises(ValueError):
        ActionValidationEvent(
            event_id="v1",
            action_ref="a1",
            user_ref="u1",
            place_ref="p1",
            decision="ACCEPTED",
            decided_at=None,
        )


# -------------------------------------------------
# Journal behavior
# -------------------------------------------------

def test_validation_journal_starts_empty():
    journal = ActionValidationJournal()
    assert journal.list_events() == []


def test_validation_journal_appends_event():
    journal = ActionValidationJournal()
    evt = make_validation()

    journal.append(evt)

    events = journal.list_events()
    assert len(events) == 1
    assert events[0] is evt


def test_validation_journal_is_append_only():
    journal = ActionValidationJournal()
    evt1 = make_validation(event_id="v1")
    evt2 = make_validation(event_id="v2", decision="REFUSED")

    journal.append(evt1)
    journal.append(evt2)

    assert [e.event_id for e in journal.list_events()] == ["v1", "v2"]


def test_validation_journal_returns_defensive_copy():
    journal = ActionValidationJournal()
    journal.append(make_validation())

    events = journal.list_events()
    events.clear()

    assert len(journal.list_events()) == 1


# -------------------------------------------------
# Singleton behavior
# -------------------------------------------------

def test_global_validation_journal_singleton():
    reset_action_validation_journal()

    evt = make_validation()
    get_action_validation_journal().append(evt)

    events = get_action_validation_journal().list_events()
    assert len(events) == 1
    assert events[0] is evt


def test_reset_validation_journal():
    reset_action_validation_journal()
    journal = get_action_validation_journal()

    journal.append(make_validation())
    assert len(journal.list_events()) == 1

    reset_action_validation_journal()
    assert journal.list_events() == []
