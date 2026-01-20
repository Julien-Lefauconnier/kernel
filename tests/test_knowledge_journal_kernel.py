# kernel/tests/test_knowledge_journal_kernel.py

import pytest

from kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from kernel.journals.knowledge.knowledge_journal import KnowledgeJournal


def test_knowledge_journal_starts_empty():
    journal = KnowledgeJournal()
    assert list(journal.iter_events()) == []


def test_knowledge_journal_append_event():
    journal = KnowledgeJournal()
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    journal.append(event)

    events = list(journal.iter_events())
    assert len(events) == 1
    assert events[0] is event


def test_knowledge_journal_preserves_order():
    journal = KnowledgeJournal()

    e1 = KnowledgeEvent.create(source="cognition", knowledge_type="fact")
    e2 = KnowledgeEvent.create(source="cognition", knowledge_type="belief")

    journal.append(e1)
    journal.append(e2)

    events = list(journal.iter_events())
    assert events == [e1, e2]


def test_knowledge_journal_is_append_only():
    journal = KnowledgeJournal()
    event = KnowledgeEvent.create(source="cognition", knowledge_type="fact")

    journal.append(event)
    events = journal.iter_events()

    assert isinstance(events, tuple)

    with pytest.raises(AttributeError):
        events.pop()

    with pytest.raises(TypeError):
        events[0] = event



def test_knowledge_journal_rejects_invalid_event():
    journal = KnowledgeJournal()

    with pytest.raises(TypeError):
        journal.append("not-an-event")
