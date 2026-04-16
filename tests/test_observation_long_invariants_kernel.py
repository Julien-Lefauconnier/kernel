# tests/test_observation_long_invariants_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.observation_long import ObservationLongEvent
from veramem_kernel.invariants.observation_long import assert_valid_observation_long_event
from veramem_kernel.invariants.observation_long.observation_long_invariants import (
    validate_observation_long_event,
)
from veramem_kernel.journals.observation_long import ObservationLongBuilder


def test_valid_observation_long_event_passes():
    event = ObservationLongBuilder(
        user_id="u1",
        source_type="governance",
        payload={"x": 1},
    ).build()

    assert_valid_observation_long_event(event)


def test_missing_user_id_fails():
    with pytest.raises(ValueError):
        ObservationLongEvent(
            user_id="",
            source_type="governance",
            payload={"x": 1},
            observed_at=datetime.now(timezone.utc),
        )


def test_missing_source_type_fails():
    with pytest.raises(ValueError):
        ObservationLongEvent(
            user_id="u1",
            source_type="",
            payload={"x": 1},
            observed_at=datetime.now(timezone.utc),
        )


def test_validate_observation_long_event_accepts_valid():
    event = ObservationLongBuilder(
        user_id="u1",
        source_type="governance",
        payload={"x": 1},
    ).build()

    validate_observation_long_event(event)


def test_validate_observation_long_event_rejects_missing_user():
    with pytest.raises(ValueError):
        ObservationLongEvent(
            user_id="",
            source_type="governance",
            payload={"x": 1},
            observed_at=datetime.now(timezone.utc),
        )


def test_validate_observation_long_event_rejects_non_dict_payload():
    with pytest.raises(TypeError):
        ObservationLongEvent(
            user_id="u1",
            source_type="governance",
            payload="not a dict",
            observed_at=datetime.now(timezone.utc),
        )
