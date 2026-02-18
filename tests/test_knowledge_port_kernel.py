# tests/test_knowledge_port_kernel.py

import pytest

from veramem_kernel.ports.knowledge_port import append_knowledge
from veramem_kernel.journals.knowledge import get_knowledge_journal
from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from veramem_kernel.journals.knowledge import (
    get_knowledge_journal,
    reset_knowledge_journal,
)



def test_append_knowledge_port_appends_event():
    reset_knowledge_journal()
    journal = get_knowledge_journal()

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


def test_reset_knowledge_journal_isolation():
    reset_knowledge_journal()
    j = get_knowledge_journal()

    e = KnowledgeEvent.create(source="t", knowledge_type="FACT")
    j.append(e)

    reset_knowledge_journal()
    j2 = get_knowledge_journal()

    print(id(get_knowledge_journal()))
    assert list(j2.iter_events()) == []
