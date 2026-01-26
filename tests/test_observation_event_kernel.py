# tests/test_observation_event_kernel.py

from datetime import datetime
from kernel.journals.observation.observation_event import ObservationEvent


def test_observation_event_is_immutable():
    event = ObservationEvent(
        user_id="u1",
        source_type="normative",
        payload={"x": 1},
        created_at=datetime.utcnow(),
    )

    assert event.user_id == "u1"
    assert event.source_type == "normative"
