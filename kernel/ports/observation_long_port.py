# kernel/ports/observation_long_port.py

from __future__ import annotations

from typing import Protocol, Sequence, Mapping, Any

from kernel.journals.observation_long.observation_long_builder import (
    ObservationLongBuilder,
)
from kernel.journals.observation_long.observation_long_event import (
    ObservationLongEvent,
)


# =============================================================================
# Writer Port
# =============================================================================

class ObservationLongWriterPort(Protocol):
    """
    Port abstraction for appending ObservationLong events.
    """

    def append(self, event: ObservationLongEvent) -> None:
        ...


def append_long_observation(
    *,
    writer: ObservationLongWriterPort,
    user_id: str,
    source_type: str,
    payload: Mapping[str, Any],
) -> None:
    """
    Kernel helper to append a longitudinal observation.

    ARVIS Contract:
    - append-only truth
    - payload must be JSON-safe
    """

    event = ObservationLongBuilder(
        user_id=user_id,
        source_type=source_type,
        payload=payload,
    ).build()

    writer.append(event)


# =============================================================================
# Reader Port
# =============================================================================

class ObservationLongReaderPort(Protocol):
    """
    Reader abstraction for longitudinal observations.

    ZKCS constraint:
    - kernel never inspects raw storage
    - reader returns already-valid events
    """

    def list_for_user(self, user_id: str) -> Sequence[ObservationLongEvent]:
        ...
