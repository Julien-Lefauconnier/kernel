# kernel/journals/action/action_validation_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ActionValidationEvent:
    """
    Kernel Action Validation Event — immutable, declarative.

    Represents the fact that a user explicitly accepted or refused
    an action at a given time.

    ❌ No execution logic
    ❌ No action mode
    ❌ No policy
    ❌ No justification

    ✔ Time-bound
    ✔ Immutable
    ✔ Zero-knowledge compatible
    """

    event_id: str
    action_ref: str

    user_ref: Optional[str]
    place_ref: Optional[str]

    decision: str  # "ACCEPTED" | "REFUSED"
    decided_at: datetime

    def __post_init__(self):
        if self.decided_at is None:
            raise ValueError(
                "ActionValidationEvent.decided_at must not be None "
                "(kernel events are strictly time-bound)."
            )
