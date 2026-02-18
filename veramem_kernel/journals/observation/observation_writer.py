# kernel/journals/observation/observation_writer.py

from datetime import datetime, timezone
from typing import Any

from veramem_kernel.journals.observation.observation_event import ObservationEvent
from veramem_kernel.journals.observation.observation_journal import ObservationJournal


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
            created_at=datetime.now(timezone.utc),
        )

        self._journal.append(event)
