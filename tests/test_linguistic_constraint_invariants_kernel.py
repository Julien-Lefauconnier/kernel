# tests/test_linguistic_constraint_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.journals.linguistic_constraint.linguistic_constraint_event import (
    LinguisticConstraintEvent,
)
from kernel.invariants.linguistic_constraint.linguistic_constraint_invariants import (
    assert_valid_linguistic_constraint_event,
)


def test_valid_constraint_event_passes_invariant():
    event = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="DECISION",
        final_act="ABSTENTION",
        reason="ACT_NOT_AUTHORIZED",
        observed_at=datetime.utcnow(),
    )

    assert_valid_linguistic_constraint_event(event)


def test_invalid_constraint_event_fails_if_no_downgrade():
    event = LinguisticConstraintEvent(
        user_id="user-1",
        place_id=None,
        conversation_mode="DEFAULT",
        original_act="INFORMATION",
        final_act="INFORMATION",
        reason=None,
        observed_at=datetime.utcnow(),
    )

    with pytest.raises(AssertionError):
        assert_valid_linguistic_constraint_event(event)
