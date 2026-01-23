# tests/test_knowledge_port_kernel.py

import pytest

from kernel.ports.knowledge_port import append_knowledge
from kernel.journals.knowledge import get_knowledge_journal
from kernel.journals.knowledge.knowledge_event import KnowledgeEvent


def test_append_knowledge_port_appends_event():
    journal = get_knowledge_journal()
    journal._events.clear()

    event = KnowledgeEvent.create(
        source="test",
        knowledge_type="FACT",
    )

    append_knowledge(event)

    events = list(journal.iter_events())
    assert len(events) == 1
    assert events[0] == event


def test_append_knowledge_port_rejects_invalid_type():
    with pytest.raises(TypeError):
        append_knowledge("not a knowledge event")
