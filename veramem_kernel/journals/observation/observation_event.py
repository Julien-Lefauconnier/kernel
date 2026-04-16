# kernel/journals/observation/observation_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ObservationEvent:
    """
    Immutable append-only observation event.

    Kernel guarantees:
    - declarative fact only
    - no inference
    - no aggregation
    - zero-knowledge payload allowed
    """

    user_id: str
    source_type: str       # e.g. "normative", "governance", "cognitive"
    payload: Any           # opaque, kernel never inspects it
    created_at: datetime
    #  optional fields
    place_id: str | None = None

    def __post_init__(self):
        if self.created_at is None:
            raise ValueError("ObservationEvent.created_at must not be None")

        if self.created_at.tzinfo is None:
            raise ValueError("ObservationEvent.created_at must be timezone-aware")

        offset = self.created_at.tzinfo.utcoffset(self.created_at)
        if offset is None or offset.total_seconds() != 0:
            raise ValueError("ObservationEvent.created_at must be UTC")
