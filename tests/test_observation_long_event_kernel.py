# tests/test_observation_long_event_kernel.py

from datetime import datetime

from kernel.journals.observation_long import ObservationLongEvent


def test_observation_long_event_is_immutable():
    event = ObservationLongEvent(
        user_id="u1",
        source_type="governance",
        payload={"drift": "high"},
        observed_at=datetime.utcnow(),
    )

    assert event.user_id == "u1"
    assert event.source_type == "governance"
    assert event.payload["drift"] == "high"
