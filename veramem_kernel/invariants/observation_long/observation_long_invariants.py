# veramem_kernel/invariants/observation_long/observation_long_invariants.py

from __future__ import annotations

from datetime import datetime
from typing import Any


def validate_observation_long_event(event: Any) -> None:
    # --------------------------
    # Identity
    # --------------------------
    if not isinstance(event.event_id, str):
        raise TypeError("ObservationLongEvent.event_id must be str")

    if len(event.event_id) < 8 or len(event.event_id) > 256:
        raise ValueError("ObservationLongEvent.event_id invalid length")

    if not event.event_id.isascii():
        raise ValueError("ObservationLongEvent.event_id must be ASCII")

    # --------------------------
    # User
    # --------------------------
    if not event.user_id:
        raise ValueError("ObservationLongEvent.user_id must not be empty")

    # --------------------------
    # Source
    # --------------------------
    if not event.source_type:
        raise ValueError("ObservationLongEvent.source_type must not be empty")

    # --------------------------
    # Timestamp
    # --------------------------
    if event.observed_at is None:
        raise ValueError("ObservationLongEvent.observed_at must be set")

    if not isinstance(event.observed_at, datetime):
        raise TypeError("ObservationLongEvent.observed_at must be datetime")

    if event.observed_at.tzinfo is None:
        raise ValueError("ObservationLongEvent.observed_at must be timezone-aware")

    offset = event.observed_at.tzinfo.utcoffset(event.observed_at)
    if offset is None or offset.total_seconds() != 0:
        raise ValueError("ObservationLongEvent.observed_at must be UTC")

    # --------------------------
    # Payload
    # --------------------------
    if not isinstance(event.payload, dict):
        raise TypeError("ObservationLongEvent.payload must be a dict")

    for k in event.payload.keys():
        if not isinstance(k, str):
            raise TypeError("ObservationLongEvent.payload keys must be strings")

        if len(k) > 128:
            raise ValueError("ObservationLongEvent.payload key too long")

        if not k.isascii():
            raise ValueError("ObservationLongEvent.payload keys must be ASCII")


def assert_valid_observation_long_event(event: Any) -> None:
    """
    Backward-compatible minimal assertion layer.

    Delegates to strict validation for now.
    """
    validate_observation_long_event(event)