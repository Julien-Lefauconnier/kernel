# kernel/journals/timeline/timeline_window.py

from dataclasses import dataclass
from typing import Optional, Dict

from .timeline_cursor import TimelineCursor


@dataclass(frozen=True)
class TimelineWindow:
    """
    Declarative temporal window over a timeline.

    A TimelineWindow defines an optional temporal slice:
    - after  : strictly after this cursor
    - before : strictly before this cursor

    Kernel guarantees:
    - immutable
    - order-safe
    - zero-knowledge
    """

    after: Optional[TimelineCursor] = None
    before: Optional[TimelineCursor] = None

    def __post_init__(self):
        if self.after and self.before:
            if self.after.timestamp >= self.before.timestamp:
                raise ValueError(
                    "TimelineWindow invariant violated: "
                    "'after' must be strictly earlier than 'before'."
                )

    def to_dict(self) -> Dict[str, Optional[str]]:
        """
        Declarative serialization for ports / adapters.
        """
        return {
            "after": self.after.timestamp.isoformat() if self.after else None,
            "before": self.before.timestamp.isoformat() if self.before else None,
        }

    def __lt__(self, other: "TimelineWindow") -> bool:
        """
        Optional ordering based on earliest bound.
        Useful for sorting windows deterministically.
        """
        if not isinstance(other, TimelineWindow):
            return NotImplemented

        self_ts = self.after.timestamp if self.after else None
        other_ts = other.after.timestamp if other.after else None

        if self_ts is None and other_ts is None:
            return False
        if self_ts is None:
            return True
        if other_ts is None:
            return False

        return self_ts < other_ts
