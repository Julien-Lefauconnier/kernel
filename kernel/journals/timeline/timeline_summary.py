# kernel/kernel/journals/timeline/timeline_summary.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .timeline_entry import TimelineEntry


@dataclass(frozen=True)
class TimelineSummary:
    """
    Canonical, fact-based summary of a timeline.

    This object:
    - aggregates timeline entries
    - exposes ordering and critical signals
    - contains no interpretation or narration
    """

    entries: List[TimelineEntry]

    total: int
    first_timestamp: Optional[datetime]
    last_timestamp: Optional[datetime]

    has_gaps: bool
    has_uncertainty: bool
    has_conflicts: bool
    has_linguistic_constraints: bool
