# kernel/journals/timeline/timeline_slice.py

from dataclasses import dataclass
from typing import Iterable, Tuple, Optional

from .timeline_entry import TimelineEntry
from .timeline_cursor import TimelineCursor


@dataclass(frozen=True)
class TimelineSlice:
    """
    Immutable, declarative slice of a timeline.

    This object represents the result of a timeline read operation.

    - No filtering logic
    - No ordering logic
    - No inference
    - Zero-knowledge compliant
    """

    entries: Tuple[TimelineEntry, ...]
    after: Optional[TimelineCursor] = None
    before: Optional[TimelineCursor] = None

    def __init__(
        self,
        *,
        entries: Iterable[TimelineEntry],
        after: Optional[TimelineCursor] = None,
        before: Optional[TimelineCursor] = None,
    ):
        object.__setattr__(self, "entries", tuple(entries))
        object.__setattr__(self, "after", after)
        object.__setattr__(self, "before", before)

