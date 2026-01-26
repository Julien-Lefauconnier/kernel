# tests/test_observation_builder_kernel.py

from datetime import datetime

from kernel.journals.observation import ObservationBuilder
from kernel.journals.observation.observation_event import ObservationEvent


class DummyNormativeSignal:
    """
    Minimal signal stub (kernel must stay API-free).
    """

    def __init__(self):
        self.user_id = "user-1"
        self.bundle_id = "bundle-123"
        self.signal_type = "DISAGREE"
        self.message = "I disagree"
        self.source = "human"
        self.created_at = datetime.utcnow()


def test_builder_creates_observation_event():
    """
    ObservationBuilder MUST convert signals into kernel ObservationEvents.

    - deterministic
    - append-only payload
    - kernel invariant
    """

    signal = DummyNormativeSignal()

    event = ObservationBuilder.from_normative_signal(signal)

    assert isinstance(event, ObservationEvent)

    assert event.user_id == "user-1"
    assert event.source_type == "normative"

    assert event.payload["bundle_id"] == "bundle-123"
    assert event.payload["signal_type"] == "DISAGREE"
    assert event.payload["message"] == "I disagree"
    assert event.payload["source"] == "human"

    assert event.created_at is not None
