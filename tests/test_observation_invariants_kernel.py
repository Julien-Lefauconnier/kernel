# tests/test_observation_invariants_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.invariants.observation.observation_invariants import (
    ObservationInvariants,
)
from veramem_kernel.journals.observation.observation_event import ObservationEvent


def test_observation_invariants_accept_valid_event():
    """
    Valid ObservationEvent must satisfy kernel invariants.
    """

    event = ObservationEvent(
        user_id="user-1",
        source_type="normative",
        payload={"signal_type": "DISAGREE"},
        created_at=datetime.now(timezone.utc),
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
        created_at=datetime.now(timezone.utc),
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
        created_at=datetime.now(timezone.utc),
    )

    assert ObservationInvariants.is_valid(event) is False

    with pytest.raises(ValueError):
        ObservationInvariants.assert_valid(event)


def test_observation_invariants_reject_missing_created_at():
    with pytest.raises(ValueError):
        ObservationEvent(
            user_id="user-1",
            source_type="normative",
            payload={},
            created_at=None,
        )