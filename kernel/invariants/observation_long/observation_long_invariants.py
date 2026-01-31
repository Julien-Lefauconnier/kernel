# kernel/invariants/observation_long/observation_long_invariants.py

from __future__ import annotations

from typing import Any
from kernel.journals.observation_long import ObservationLongEvent


def assert_valid_observation_long_event(event: ObservationLongEvent) -> None:
    """
    Kernel invariant checks for ObservationLongEvent.

    Enforces:
    - user_id must be set
    - source_type must be non-empty
    """

    if not event.user_id:
        raise ValueError("ObservationLongEvent.user_id must not be empty")

    if not event.source_type:
        raise ValueError("ObservationLongEvent.source_type must not be empty")


def validate_observation_long_event(event: ObservationLongEvent) -> None:
    if not event.user_id:
        raise ValueError("ObservationLongEvent.user_id must not be empty")

    if not event.source_type:
        raise ValueError("ObservationLongEvent.source_type must not be empty")

    if event.observed_at is None:
        raise ValueError("ObservationLongEvent.observed_at must be set")

    if not isinstance(event.payload, dict):
        raise TypeError("ObservationLongEvent.payload must be a dict")

    for k in event.payload.keys():
        if not isinstance(k, str):
            raise TypeError("ObservationLongEvent.payload keys must be strings")
