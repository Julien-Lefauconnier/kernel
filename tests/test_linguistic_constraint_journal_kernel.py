# tests/test_linguistic_constraint_journal_kernel.py

from datetime import datetime, timedelta

from kernel.journals.linguistic_constraint.linguistic_constraint_event import (
    LinguisticConstraintEvent,
)
from kernel.journals.linguistic_constraint.linguistic_constraint_journal_in_memory import (
    InMemoryLinguisticConstraintJournal,
)


def test_journal_appends_and_lists_events():
    journal = InMemoryLinguisticConstraintJournal()

    event = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason="ACT_NOT_AUTHORIZED",
        observed_at=datetime.utcnow(),
    )

    journal.append(event)

    events = journal.list_for_user(user_id="user-1")

    assert len(events) == 1
    assert events[0].final_act == "ABSTENTION"


def test_journal_respects_since_filter():
    journal = InMemoryLinguisticConstraintJournal()

    now = datetime.utcnow()

    old = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason=None,
        observed_at=now,
    )

    journal.append(old)

    future = now + timedelta(days=1)

    events = journal.list_for_user(user_id="user-1", since=future)

    assert events == []


def test_journal_respects_place_filter():
    journal = InMemoryLinguisticConstraintJournal()

    e1 = LinguisticConstraintEvent(
        user_id="user-1",
        place_id="home",
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason=None,
        observed_at=datetime.utcnow(),
    )

    e2 = LinguisticConstraintEvent(
        user_id="user-1",
        place_id="work",
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason=None,
        observed_at=datetime.utcnow(),
    )

    journal.append(e1)
    journal.append(e2)

    events = journal.list_for_user(user_id="user-1", place_id="home")

    assert len(events) == 1
    assert events[0].place_id == "home"
