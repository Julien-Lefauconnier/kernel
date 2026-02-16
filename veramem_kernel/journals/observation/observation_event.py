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
