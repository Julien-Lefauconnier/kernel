# kernel/journals/timeline/timeline_query.py

from dataclasses import dataclass
from typing import Optional

from .timeline_window import TimelineWindow


@dataclass(frozen=True)
class TimelineQuery:
    """
    Declarative timeline query.

    This object describes *how* a timeline should be read,
    without performing any read itself.

    - Immutable
    - Zero-knowledge
    - Kernel-pure
    """

    window: Optional[TimelineWindow] = None
    limit: Optional[int] = None
    direction: str = "forward"  # "forward" | "backward"

    def __post_init__(self):
        if self.limit is not None:
            if not isinstance(self.limit, int) or self.limit <= 0:
                raise ValueError(
                    "TimelineQuery.limit must be a positive integer"
                )

        if self.direction not in {"forward", "backward"}:
            raise ValueError(
                "TimelineQuery.direction must be 'forward' or 'backward'"
            )
