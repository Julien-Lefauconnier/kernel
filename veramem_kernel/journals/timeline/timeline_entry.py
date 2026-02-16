# kernel/journals/timeline/timeline_entry.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

from .timeline_types import TimelineEntryType

class TimelineEntryNature(str, Enum):
    """
    Nature of a timeline entry.

    EVENT:
        A punctual, observable occurrence.
    STATE:
        A declarative snapshot of a system or cognitive state.
    """

    EVENT = "event"
    STATE = "state"


@dataclass(frozen=True)
class TimelineEntry:
    entry_id: str
    created_at: datetime
    type: TimelineEntryType
    title: str
    description: Optional[str]
    action_id: Optional[str]
    place_id: Optional[str]


    # 🧭 Declarative traceability reference
    origin_ref: Optional[str] = None

    # 🧩 Entry nature (EVENT / STATE)
    nature: TimelineEntryNature = TimelineEntryNature.EVENT

    def __post_init__(self):
        """
        Enforce Timeline invariants.

        - created_at must always be defined
        - timeline entries are immutable and declarative
        """

        if self.created_at is None:
            raise ValueError(
                "TimelineEntry.created_at must not be None "
                "(timeline entries are strictly time-bound)."
            )

    @property
    def timestamp(self) -> datetime:
        """
        Canonical timeline timestamp.

        Alias for created_at to provide a stable,
        semantic API for consumers (tests, API, debug).
        """
        return self.created_at

    # ------------------------------------------------------------------
    # ⚠️ Unsafe constructor (tests / legacy only)
    # ------------------------------------------------------------------
    @classmethod
    def unsafe(
        cls,
        *,
        entry_id: str,
        type: TimelineEntryType,
        title: str,
        description: Optional[str],
        action_id: Optional[str],
        place_id: Optional[str] = None,
        origin_ref: Optional[str] = None,
        nature: TimelineEntryNature = TimelineEntryNature.EVENT,
        created_at: Optional[datetime] = None,
    ) -> "TimelineEntry":
        """
        Unsafe constructor for tests and legacy code.

        This bypasses strict temporal invariants and MUST NOT
        be used in production code.
        """
        return cls(
            entry_id=entry_id,
            created_at=created_at or datetime.utcnow(),
            type=type,
            title=title,
            description=description,
            action_id=action_id,
            place_id=place_id,
            origin_ref=origin_ref,
            nature=nature,
        )

    @property
    def label(self) -> str:
        """
        Human-readable label for timeline entries.

        Canonical semantic alias used by tests, debug views
        and governance projections.
        """
        if self.description:
            return self.description
        return self.title
