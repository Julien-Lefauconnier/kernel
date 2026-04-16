# kernel/journals/action/action_event.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from uuid import uuid4
import hashlib
import json


@dataclass(frozen=True)
class ActionEvent:
    """
    Kernel Action Event — immutable, declarative, replayable.

    This event represents the fact that an action decision
    entered the system at a given time.

    - No cognition
    - No conflicts
    - No presentation
    - No policy

    ✔ Time-bound
    ✔ Immutable
    ✔ Zero-knowledge compatible
    """

    # Technical identity
    event_id: str
    created_at: datetime

    # Opaque references (never interpreted here)
    user_ref: Optional[str] = None
    place_ref: Optional[str] = None
    action_ref: Optional[str] = None

    # Declarative intent
    intent: Optional[str] = None
    mode: Optional[str] = None  # "manual" | "assisted" | "automatic"

    # Optional opaque metadata (hashes, flags, debug traces)
    extras: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.created_at is None:
            raise ValueError(
                "ActionEvent.created_at must not be None "
                "(kernel events are strictly time-bound)."
            )
    
    @property
    def timestamp(self) -> datetime:
        return self.created_at
    
    @classmethod
    def create(
        cls,
        *,
        user_ref: Optional[str] = None,
        place_ref: Optional[str] = None,
        action_ref: Optional[str] = None,
        intent: Optional[str] = None,
        mode: Optional[str] = None,
        extras: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ) -> "ActionEvent":
        """
        Industrial deterministic factory.

        Guarantees:
        - replay safety
        - idempotence
        - stable identity
        """

        if created_at is None:
            created_at = datetime.now(timezone.utc)

        extras = extras or {}

        # 🔐 Stable deterministic identity
        payload = {
            "user_ref": user_ref,
            "place_ref": place_ref,
            "action_ref": action_ref,
            "intent": intent,
            "mode": mode,
            "extras": extras,
            "created_at": created_at.isoformat(),
        }

        serialized = json.dumps(payload, sort_keys=True)
        event_id = hashlib.sha256(serialized.encode()).hexdigest()

        return cls(
            event_id=event_id,
            created_at=created_at,
            user_ref=user_ref,
            place_ref=place_ref,
            action_ref=action_ref,
            intent=intent,
            mode=mode,
            extras=extras,
        )


