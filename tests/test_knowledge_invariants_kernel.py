# kernel/tests/test_knowledge_invariants_kernel.py


import pytest
from datetime import datetime

from kernel.journals.knowledge.knowledge_event import KnowledgeEvent
from kernel.invariants.knowledge.knowledge_invariants import (
    assert_has_timestamp,
    assert_has_source,
    assert_has_knowledge_type,
)


def make_event(**overrides):
    base = dict(
        source="cognition",
        knowledge_type="fact",
        created_at=datetime.utcnow(),
    )
    base.update(overrides)
    return KnowledgeEvent.create(**base)


def test_valid_knowledge_event_passes_all_invariants():
    event = make_event()

    assert_has_timestamp(event)
    assert_has_source(event)
    assert_has_knowledge_type(event)


def test_timestamp_is_always_set_by_factory():
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    assert event.created_at is not None


def test_empty_source_is_rejected():
    event = make_event(source="")

    with pytest.raises(ValueError):
        assert_has_source(event)


def test_missing_knowledge_type_is_rejected():
    event = make_event(knowledge_type=None)

    with pytest.raises(ValueError):
        assert_has_knowledge_type(event)
