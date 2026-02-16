# kernel/journals/timeline/timeline_view.py

from dataclasses import dataclass
from typing import Tuple

from .timeline_entry import TimelineEntry
from .timeline_view_types import TimelineViewRole


@dataclass(frozen=True)
class TimelineView:
    """
    Read-only projection of a canonical timeline.

    - Immutable
    - Declarative
    - Zero-knowledge compliant
    """

    role: TimelineViewRole
    entries: Tuple[TimelineEntry, ...]
