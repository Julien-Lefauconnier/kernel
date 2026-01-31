# tests/test_observation_long_port_append_kernel.py

from kernel.journals.observation_long import (
    ObservationLongJournalInMemory,
    ObservationLongWriter,
)
from kernel.ports.observation_long_port import append_long_observation


def test_append_long_observation_port_helper():
    journal = ObservationLongJournalInMemory()
    writer = ObservationLongWriter(journal=journal)

    append_long_observation(
        writer=writer,
        user_id="u42",
        source_type="cognitive",
        payload={"marker": "attention_drift"},
    )

    events = list(journal.list_for_user(user_id="u42"))
    assert len(events) == 1
    assert events[0].payload["marker"] == "attention_drift"
