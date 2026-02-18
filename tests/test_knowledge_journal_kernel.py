# kernel/tests/test_knowledge_journal_kernel.py

import pytest
from datetime import datetime, timezone, timezone, timedelta


from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from veramem_kernel.journals.knowledge.knowledge_journal import KnowledgeJournal


# ------------
import inspect
from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from veramem_kernel.journals.knowledge.knowledge_journal import KnowledgeJournal

def test_debug():
    print(inspect.getsource(KnowledgeEvent.create))

def test__debug_journal_source():
    print(inspect.getsource(KnowledgeJournal.append))

# ----------------

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

def test_knowledge_journal_rejects_non_monotonic():
    j = KnowledgeJournal()
    t2 = datetime(2024,1,2,tzinfo=timezone.utc)
    t1 = datetime(2024,1,1,tzinfo=timezone.utc)
    e2 = KnowledgeEvent.create(source="cognition", knowledge_type="fact", created_at=t2)
    e1 = KnowledgeEvent.create(source="cognition", knowledge_type="fact", created_at=t1)
    j.append(e2)
    with pytest.raises(ValueError):
        j.append(e1)


def test_knowledge_journal_rejects_duplicate_event_id():
    j = KnowledgeJournal()
    t = datetime.now(timezone.utc)
    e1 = KnowledgeEvent.create(event_id="x", source="cognition", knowledge_type="fact", created_at=t)
    e2 = KnowledgeEvent.create(event_id="x", source="cognition", knowledge_type="fact", created_at=t)
    j.append(e1)
    with pytest.raises(ValueError):
        j.append(e2)


def test_knowledge_journal_rejects_future_drift():
    j = KnowledgeJournal()
    future = datetime.now(timezone.utc) + timedelta(hours=1)
    e = KnowledgeEvent.create(source="cognition", knowledge_type="fact", created_at=future)
    with pytest.raises(ValueError):
        j.append(e)
