# tests/test_observation_long_writer_kernel.py

from kernel.journals.observation_long import (
    ObservationLongJournalInMemory,
    ObservationLongWriter,
    ObservationLongBuilder,
)


def test_writer_appends_event():
    journal = ObservationLongJournalInMemory()
    writer = ObservationLongWriter(journal=journal)

    event = ObservationLongBuilder(
        user_id="u1",
        source_type="normative",
        payload={"x": 1},
    ).build()

    writer.append(event)

    stored = list(journal.list_for_user(user_id="u1"))
    assert len(stored) == 1
    assert stored[0].payload["x"] == 1
