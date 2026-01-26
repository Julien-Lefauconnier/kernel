# tests/test_normative_pattern_builder_kernel.py

from datetime import datetime

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.patterns.normative_pattern_builder import (
    NormativePatternBuilder,
)


class DummySignal:
    def __init__(self, signal_type):
        self.signal_type = signal_type


def test_normative_pattern_projection():
    events = [
        ObservationEvent(
            user_id="u1",
            source_type="normative",
            payload=DummySignal("DISAGREE"),
            created_at=datetime.utcnow(),
        ),
        ObservationEvent(
            user_id="u1",
            source_type="normative",
            payload=DummySignal("DISAGREE"),
            created_at=datetime.utcnow(),
        ),
    ]

    patterns = NormativePatternBuilder.build(events=events)

    assert len(patterns) == 1
    assert patterns[0].occurrences == 2
    assert patterns[0].signal_type == "DISAGREE"
