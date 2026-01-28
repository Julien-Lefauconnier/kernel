# kernel/journals/observation/observation_journal.py

from datetime import datetime
from typing import List, Protocol

from kernel.journals.observation.observation_event import ObservationEvent


class ObservationJournal(Protocol):
    """
    Append-only journal for longitudinal observations.

    Kernel responsibilities:
    - persist immutable facts
    - list deterministically
    """

    def append(self, event: ObservationEvent) -> None:
        """
        Record an observation event (append-only).
        """
        ...

    def list_for_user(
        self,
        *,
        user_id: str,
        place_id: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> List[ObservationEvent]:
        """
        Deterministic observation listing.

        Optional temporal filtering only.
        """
        ...
