# kernel/journals/timeline/timeline_cursor.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class TimelineCursor:
    """
    Immutable, comparable cursor representing a position
    in the timeline.

    Kernel-level temporal primitive:
    - pure value object
    - no domain logic
    """

    timestamp: datetime

    # --------------------------------------------------
    # Invariants
    # --------------------------------------------------
    def __post_init__(self):
        if self.timestamp is None:
            raise ValueError(
                "TimelineCursor.timestamp must not be None"
            )

    # --------------------------------------------------
    # Comparisons
    # --------------------------------------------------
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimelineCursor):
            return False
        return self.timestamp == other.timestamp

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, TimelineCursor):
            raise TypeError(
                "TimelineCursor can only be compared with TimelineCursor"
            )
        return self.timestamp < other.timestamp

    # --------------------------------------------------
    # Serialization
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "TimelineCursor":
        try:
            ts = datetime.fromisoformat(payload["timestamp"])
        except Exception as exc:
            raise ValueError(
                "Invalid TimelineCursor payload"
            ) from exc

        return cls(timestamp=ts)
