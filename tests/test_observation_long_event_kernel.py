# tests/test_observation_long_event_kernel.py

from datetime import datetime, timezone

from veramem_kernel.journals.observation_long import ObservationLongEvent


def test_observation_long_event_is_immutable():
    event = ObservationLongEvent(
        user_id="u1",
        source_type="governance",
        payload={"drift": "high"},
        observed_at=datetime.now(timezone.utc),
    )

    assert event.user_id == "u1"
    assert event.source_type == "governance"
    assert event.payload["drift"] == "high"
