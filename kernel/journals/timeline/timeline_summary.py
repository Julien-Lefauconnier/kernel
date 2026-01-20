# kernel/journals/timeline/timeline_summary.py

from typing import List, Optional

from .timeline_entry import TimelineEntry
from .timeline_types import TimelineEntryType


class TimelineSummary:
    """
    Canonical, fact-based summary of a timeline.

    This object:
    - aggregates timeline entries
    - exposes ordering and critical signals
    - contains no interpretation or narration
    """

    def __init__(
        self,
        *,
        entries: List[TimelineEntry],
        total: int,
        first_timestamp: Optional,
        last_timestamp: Optional,
        has_gaps: bool,
        has_uncertainty: bool,
        has_conflicts: bool,
        has_linguistic_constraints: bool,
    ):
        self.entries = entries
        self.total = total
        self.first_timestamp = first_timestamp
        self.last_timestamp = last_timestamp
        self.has_gaps = has_gaps
        self.has_uncertainty = has_uncertainty
        self.has_conflicts = has_conflicts
        self.has_linguistic_constraints = has_linguistic_constraints


def summarize_timeline(
    *,
    entries: List[TimelineEntry],
) -> TimelineSummary:
    """
    Build a canonical TimelineSummary from timeline entries.

    - Pure function
    - Deterministic
    - Zero-knowledge compliant
    """

    if not entries:
        return TimelineSummary(
            entries=[],
            total=0,
            first_timestamp=None,
            last_timestamp=None,
            has_gaps=False,
            has_uncertainty=False,
            has_conflicts=False,
            has_linguistic_constraints=False,
        )

    ordered = sorted(entries, key=lambda e: e.created_at)

    has_conflicts = False
    has_uncertainty = False
    has_gaps = False
    has_linguistic_constraints = False

    for entry in ordered:
        if entry.type == TimelineEntryType.CONFLICT:
            has_conflicts = True

        if entry.type in {
            TimelineEntryType.UNCERTAINTY_FRAME,
            TimelineEntryType.REASONING_GAP,
            TimelineEntryType.SYSTEM_NOTICE,
        }:
            has_uncertainty = True

        if entry.type == TimelineEntryType.REASONING_GAP:
            has_gaps = True

        if entry.type == TimelineEntryType.LINGUISTIC_CONSTRAINT:
            has_linguistic_constraints = True

    return TimelineSummary(
        entries=ordered,
        total=len(ordered),
        first_timestamp=ordered[0].created_at,
        last_timestamp=ordered[-1].created_at,
        has_gaps=has_gaps,
        has_uncertainty=has_uncertainty,
        has_conflicts=has_conflicts,
        has_linguistic_constraints=has_linguistic_constraints,
    )
