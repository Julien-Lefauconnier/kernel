# tests/test_observation_journal_kernel.py

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.observation_journal_in_memory import (
    InMemoryObservationJournal,
)
from datetime import datetime


def test_append_and_list_observations():
    journal = InMemoryObservationJournal()

    journal.append(
        ObservationEvent(
            user_id="u1",
            source_type="normative",
            payload="x",
            created_at=datetime.utcnow(),
        )
    )

    results = journal.list_for_user(user_id="u1")
    assert len(results) == 1
