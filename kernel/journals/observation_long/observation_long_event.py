# kernel/journals/observation_long/observation_long_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ObservationLongEvent:
    """
    Immutable longitudinal observation event.

    Kernel Contract:
    - append-only truth
    - payload is fully opaque
    - no inference
    - post-hoc only

    This event records that something longitudinal was observed
    (governance drift, cognitive stability, normative evolution...).
    """

    user_id: str
    source_type: str
    payload: Any
    observed_at: datetime
