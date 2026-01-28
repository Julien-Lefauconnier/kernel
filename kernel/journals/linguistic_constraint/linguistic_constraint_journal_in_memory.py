# kernel/journals/linguistic_constraint/linguistic_constraint_journal_in_memory.py

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .linguistic_constraint_event import LinguisticConstraintEvent
from .linguistic_constraint_journal import LinguisticConstraintJournal


class InMemoryLinguisticConstraintJournal(LinguisticConstraintJournal):
    """
    Reference kernel implementation.

    - append-only
    - deterministic ordering
    - no dedup
    """

    def __init__(self):
        self._events: List[LinguisticConstraintEvent] = []

    def append(self, event: LinguisticConstraintEvent) -> None:
        self._events.append(event)

    def list_for_user(
        self,
        *,
        user_id: str,
        place_id: str | None = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ) -> List[LinguisticConstraintEvent]:

        results = [e for e in self._events if e.user_id == user_id]

        if place_id is not None:
            results = [e for e in results if e.place_id == place_id]

        if since is not None:
            results = [e for e in results if e.observed_at >= since]

        if until is not None:
            results = [e for e in results if e.observed_at <= until]

        return results

