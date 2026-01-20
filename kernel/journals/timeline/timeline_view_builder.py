# kernel/journals/timeline/timeline_view_builder.py

from typing import Iterable, List

from .timeline_entry import TimelineEntry, TimelineEntryNature
from .timeline_types import TimelineEntryType
from .timeline_view import TimelineView
from .timeline_view_types import TimelineViewRole


class TimelineViewBuilder:
    """
    Stateless builder for kernel timeline views.

    - Pure
    - Deterministic
    - No policy
    - No access control
    """

    @staticmethod
    def build(
        *,
        role: TimelineViewRole,
        entries: Iterable[TimelineEntry],
    ) -> TimelineView:
        source = list(entries)

        if role == TimelineViewRole.TRACE_FACTUELLE:
            filtered = [
                entry for entry in source
                if entry.type in {
                    TimelineEntryType.ACTION_PROPOSED,
                    TimelineEntryType.ACTION_VALIDATED,
                    TimelineEntryType.ACTION_REFUSED,
                    TimelineEntryType.ACTION_BLOCKED,
                    TimelineEntryType.DOCUMENT_ACCESSED,
                    TimelineEntryType.DOCUMENT_EDITED,
                    TimelineEntryType.HUMAN_FEEDBACK,
                }
            ]

        elif role in {
            TimelineViewRole.ETAT_COGNITIF_SYSTEME,
            TimelineViewRole.AWARENESS_POST_COGNITIVE,
            TimelineViewRole.GOUVERNANCE_HUMAINE,
        }:
            filtered = [
                entry for entry in source
                if entry.nature == TimelineEntryNature.STATE
            ]

        else:
            filtered = []

        # ⚠️ Important : preserve order + immutability
        return TimelineView(
            role=role,
            entries=tuple(filtered),
        )

    @staticmethod
    def build_all(
        *,
        entries: Iterable[TimelineEntry],
    ) -> List[TimelineView]:
        """
        Build one view per TimelineViewRole.
        """
        return [
            TimelineViewBuilder.build(
                role=role,
                entries=entries,
            )
            for role in TimelineViewRole
        ]
