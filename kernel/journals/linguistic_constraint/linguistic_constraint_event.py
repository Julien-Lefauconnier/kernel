# kernel/journals/linguistic_constraint/linguistic_constraint_event.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class LinguisticConstraintEvent:
    """
    Kernel factual event: a deterministic constraint was applied
    to a linguistic act post cognitive gate.

    - append-only
    - non-executable
    - no inference
    """

    user_id: str
    place_id: Optional[str]

    conversation_mode: str

    original_act: str
    final_act: str

    reason: Optional[str]

    observed_at: datetime

    def __post_init__(self):
        if self.reason == "ACT_NOT_AUTHORIZED_FOR_MODE":
            object.__setattr__(
                self,
                "reason",
                "ACT_NOT_AUTHORIZED_FOR_CONVERSATION_MODE",
            )