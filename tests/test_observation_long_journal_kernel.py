# tests/test_observation_long_journal_kernel.py

from datetime import datetime, timezone

from veramem_kernel.journals.observation_long import (
    ObservationLongEvent,
    ObservationLongJournalInMemory,
)


def test_append_and_list_observation_long_events():
    journal = ObservationLongJournalInMemory()

    e1 = ObservationLongEvent(
        user_id="u1",
        source_type="normative",
        payload={"rule": "no_personal_data"},
        observed_at=datetime.now(timezone.utc),
    )

    e2 = ObservationLongEvent(
        user_id="u1",
        source_type="cognitive",
        payload={"stability": "low"},
        observed_at=datetime.now(timezone.utc),
    )

    journal.append(e1)
    journal.append(e2)

    events = list(journal.list_for_user(user_id="u1"))

    assert len(events) == 2
    assert events[0] == e1
    assert events[1] == e2
