# kernel/journals/observation/observation_writer.py

from datetime import datetime
from typing import Any

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.observation_journal import ObservationJournal


class ObservationWriter:
    """
    Explicit append-only writer.

    Kernel guarantees:
    - no branching
    - no inference
    - no interpretation
    """

    def __init__(self, *, journal: ObservationJournal):
        self._journal = journal

    def record(
        self,
        *,
        user_id: str,
        source_type: str,
        payload: Any,
    ) -> None:

        event = ObservationEvent(
            user_id=user_id,
            source_type=source_type,
            payload=payload,
            created_at=datetime.utcnow(),
        )

        self._journal.append(event)
