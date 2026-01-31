# kernel/journals/observation_long/observation_long_journal_in_memory.py

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, List

from .observation_long_event import ObservationLongEvent
from .observation_long_journal import ObservationLongJournal


class ObservationLongJournalInMemory(ObservationLongJournal):
    """
    In-memory reference implementation of ObservationLongJournal.

    Used for:
    - kernel unit tests
    - local dev runtime
    - contract validation

    Not persistent.
    """

    def __init__(self) -> None:
        self._events: dict[str, List[ObservationLongEvent]] = defaultdict(list)

    def append(self, event: ObservationLongEvent) -> None:
        self._events[event.user_id].append(event)

    def list_for_user(self, *, user_id: str) -> Iterable[ObservationLongEvent]:
        return list(self._events.get(user_id, []))
