# tests/test_observation_long_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.journals.observation_long import ObservationLongEvent
from kernel.invariants.observation_long import assert_valid_observation_long_event
from kernel.invariants.observation_long.observation_long_invariants import (
    validate_observation_long_event,
)
from kernel.journals.observation_long import ObservationLongBuilder


def test_valid_observation_long_event_passes():
    event = ObservationLongBuilder(
        user_id="u1",
        source_type="governance",
        payload={"x": 1},
    ).build()

    assert_valid_observation_long_event(event)


def test_missing_user_id_fails():
    event = ObservationLongEvent(
        user_id="",
        source_type="governance",
        payload={"x": 1},
        observed_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError):
        assert_valid_observation_long_event(event)


def test_missing_source_type_fails():
    event = ObservationLongEvent(
        user_id="u1",
        source_type="",
        payload={"x": 1},
        observed_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError):
        validate_observation_long_event(event)


def test_validate_observation_long_event_accepts_valid():
    event = ObservationLongBuilder(
        user_id="u1",
        source_type="governance",
        payload={"x": 1},
    ).build()

    validate_observation_long_event(event)


def test_validate_observation_long_event_rejects_missing_user():
    event = ObservationLongEvent(
        user_id="",
        source_type="governance",
        payload={"x": 1},
        observed_at=datetime.utcnow(),
    )

    with pytest.raises(ValueError):
        validate_observation_long_event(event)



def test_validate_observation_long_event_rejects_non_dict_payload():
    event = ObservationLongEvent(
        user_id="u1",
        source_type="governance",
        payload="not a dict",
        observed_at=datetime.utcnow(),
    )

    with pytest.raises(TypeError):
        validate_observation_long_event(event)
