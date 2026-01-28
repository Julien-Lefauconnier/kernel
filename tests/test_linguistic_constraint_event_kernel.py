# tests/test_linguistic_constraint_event_kernel.py

from datetime import datetime

from kernel.journals.linguistic_constraint.linguistic_constraint_event import (
    LinguisticConstraintEvent,
)


def test_linguistic_constraint_event_is_frozen_and_factual():
    event = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason="ACT_NOT_AUTHORIZED",
        observed_at=datetime.utcnow(),
    )

    assert event.user_id == "user-1"
    assert event.original_act == "DECISION"
    assert event.final_act == "ABSTENTION"

def test_linguistic_constraint_event_canonicalizes_old_reason():
    event = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason="ACT_NOT_AUTHORIZED_FOR_MODE",  # legacy
        observed_at=datetime.utcnow(),
    )

    assert event.reason == "ACT_NOT_AUTHORIZED_FOR_CONVERSATION_MODE"
