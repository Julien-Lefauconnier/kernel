# kernel/invariants/linguistic_constraint/linguistic_constraint_invariants.py

"""
Kernel invariants — Linguistic Constraint

This module defines non-negotiable constraints:

- events are factual
- append-only semantics
- no inference
- deterministic constraint enforcement only
"""

from kernel.journals.linguistic_constraint.linguistic_constraint_event import (
    LinguisticConstraintEvent,
)


def assert_valid_linguistic_constraint_event(
    event: LinguisticConstraintEvent,
) -> None:
    """
    Kernel invariant: linguistic constraint events must be explicit,
    factual and deterministic.
    """

    assert event.user_id, "user_id is required"

    assert event.original_act, "original_act must be present"
    assert event.final_act, "final_act must be present"

    assert (
        event.original_act != event.final_act
    ), "constraint event must reflect an actual downgrade"

    assert event.conversation_mode, "conversation_mode is required"

    # Reason is optional but if present must be non-empty
    if event.reason is not None:
        assert event.reason.strip() != "", "reason cannot be blank"
