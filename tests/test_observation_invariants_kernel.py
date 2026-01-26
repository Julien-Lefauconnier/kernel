# tests/test_observation_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.invariants.observation.observation_invariants import (
    ObservationInvariants,
)
from kernel.journals.observation.observation_event import ObservationEvent


def test_observation_invariants_accept_valid_event():
    """
    Valid ObservationEvent must satisfy kernel invariants.
    """

    event = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={"signal_type": "DISAGREE"},
        created_at=datetime.utcnow(),
    )

    assert ObservationInvariants.is_valid(event) is True
    ObservationInvariants.assert_valid(event)


def test_observation_invariants_reject_missing_user_id():
    """
    user_id is mandatory.
    """

    event = ObservationEvent(
        user_id="",
        source_type="normative",
        payload={},
        created_at=datetime.utcnow(),
    )

    assert ObservationInvariants.is_valid(event) is False

    with pytest.raises(ValueError):
        ObservationInvariants.assert_valid(event)


def test_observation_invariants_reject_missing_source_type():
    """
    source_type is mandatory.
    """

    event = ObservationEvent(
        user_id="user-1",
        source_type="",
        payload={},
        created_at=datetime.utcnow(),
    )

    assert ObservationInvariants.is_valid(event) is False

    with pytest.raises(ValueError):
        ObservationInvariants.assert_valid(event)


def test_observation_invariants_reject_missing_created_at():
    """
    created_at must always exist (append-only traceability).
    """

    event = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={},
        created_at=None,  # type: ignore[arg-type]
    )

    assert ObservationInvariants.is_valid(event) is False

    with pytest.raises(ValueError):
        ObservationInvariants.assert_valid(event)