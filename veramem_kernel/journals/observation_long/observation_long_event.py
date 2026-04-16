# veramem_kernel/journals/observation_long/observation_long_event.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import hashlib
import json

from veramem_kernel.invariants.observation_long.observation_long_invariants import (
    validate_observation_long_event,
)


@dataclass(frozen=True)
class ObservationLongEvent:

    observed_at: datetime
    user_id: str
    source_type: str
    payload: Dict[str, Any]

    event_id: Optional[str] = None

    def __post_init__(self):

        # 1. Generate ID first
        if self.event_id is None:
            raw = {
                "user_id": self.user_id,
                "source_type": self.source_type,
                "payload": self.payload,
                "observed_at": self.observed_at.isoformat(),
            }

            serialized = json.dumps(raw, sort_keys=True)
            eid = hashlib.sha256(serialized.encode()).hexdigest()

            object.__setattr__(self, "event_id", eid)

        # 2. THEN validate
        validate_observation_long_event(self)

    @property
    def timestamp(self) -> datetime:
        """
        Canonical timestamp for unified timeline compatibility.

        Timeline consumers should rely on `timestamp` as the stable
        temporal accessor across heterogeneous kernel events.
        """
        return self.observed_at

    @classmethod
    def create(
        cls,
        *,
        user_id: str,
        source_type: str,
        payload: Dict[str, Any],
        observed_at: Optional[datetime] = None,
    ) -> "ObservationLongEvent":
        if observed_at is None:
            observed_at = datetime.now(timezone.utc)

        raw = {
            "user_id": user_id,
            "source_type": source_type,
            "payload": payload,
            "observed_at": observed_at.isoformat(),
        }

        serialized = json.dumps(raw, sort_keys=True)
        event_id = hashlib.sha256(serialized.encode()).hexdigest()

        return cls(
            event_id=event_id,
            observed_at=observed_at,
            user_id=user_id,
            source_type=source_type,
            payload=payload,
        )
