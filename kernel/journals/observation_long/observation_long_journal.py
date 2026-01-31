# kernel/journals/observation_long/observation_long_journal.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .observation_long_event import ObservationLongEvent


class ObservationLongJournal(ABC):
    """
    Append-only journal for longitudinal observations.

    Kernel Contract:
    - events are append-only
    - queries are post-hoc
    - no aggregation or inference inside kernel
    """

    @abstractmethod
    def append(self, event: ObservationLongEvent) -> None:
        """
        Record a longitudinal observation event.
        """
        raise NotImplementedError

    @abstractmethod
    def list_for_user(self, *, user_id: str) -> Iterable[ObservationLongEvent]:
        """
        List all observation long events for a given user.
        """
        raise NotImplementedError
