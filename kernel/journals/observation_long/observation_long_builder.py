# kernel/journals/observation_long/observation_long_builder.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Any

from kernel.journals.observation_long.observation_long_event import (
    ObservationLongEvent,
)
from kernel.invariants.observation_long.observation_long_invariants import (
    validate_observation_long_event,
)


@dataclass
class ObservationLongBuilder:
    """
    Declarative builder for ObservationLongEvent.

    Contract:
    - payload must be JSON-safe
    - zero inference
    - append-only kernel truth
    """

    user_id: str
    source_type: str
    payload: Mapping[str, Any]

    def build(self) -> ObservationLongEvent:
        event = ObservationLongEvent(
            user_id=self.user_id,
            source_type=self.source_type,
            payload=dict(self.payload),
            observed_at=datetime.utcnow(),
        )

        validate_observation_long_event(event)
        return event
