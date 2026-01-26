# kernel/journals/observation/observation_journal_in_memory.py

from datetime import datetime
from typing import List

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.observation_journal import ObservationJournal


class InMemoryObservationJournal(ObservationJournal):
    """
    Reference kernel implementation.

    - append-only
    - no deduplication
    - deterministic ordering
    """

    def __init__(self):
        self._events: List[ObservationEvent] = []

    def append(self, event: ObservationEvent) -> None:
        self._events.append(event)

    def list_for_user(
        self,
        *,
        user_id: str,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> List[ObservationEvent]:

        results = [e for e in self._events if e.user_id == user_id]

        if since is not None:
            results = [e for e in results if e.created_at >= since]

        if until is not None:
            results = [e for e in results if e.created_at <= until]

        return results
