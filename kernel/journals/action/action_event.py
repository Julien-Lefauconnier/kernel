# kernel/journals/action/action_event.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class ActionEvent:
    """
    Kernel Action Event — immutable, declarative, replayable.

    This event represents the fact that an action decision
    entered the system at a given time.

    ❌ No cognition
    ❌ No conflicts
    ❌ No presentation
    ❌ No policy

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
