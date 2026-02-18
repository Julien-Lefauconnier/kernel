# kernel/tests/test_knowledge_event_kernel.py

from datetime import datetime, timezone, timezone
import pytest

from veramem_kernel.journals.knowledge.knowledge_event import KnowledgeEvent


def test_knowledge_event_is_immutable():
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    with pytest.raises(Exception):
        event.source = "other"


def test_knowledge_event_has_auto_id_and_timestamp():
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    assert event.event_id is not None
    assert isinstance(event.event_id, str)
    assert event.created_at is not None
    assert isinstance(event.created_at, datetime)


def test_knowledge_event_preserves_explicit_values():
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)

    event = KnowledgeEvent.create(
        event_id="event-123",
        created_at=now,
        source="cognition",
        knowledge_type="belief",
        user_ref="user-1",
        place_ref="place-1",
    )

    assert event.event_id == "event-123"
    assert event.created_at == now
    assert event.source == "cognition"
    assert event.knowledge_type == "belief"
    assert event.user_ref == "user-1"
    assert event.place_ref == "place-1"


def test_knowledge_event_has_no_payload_or_snapshot():
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    forbidden_attrs = [
        "payload",
        "snapshot",
        "state",
        "content",
        "value",
    ]

    for attr in forbidden_attrs:
        assert not hasattr(event, attr)


def test_knowledge_event_is_pure_data_object():
    event = KnowledgeEvent.create(
        source="cognition",
        knowledge_type="fact",
    )

    assert callable(event.create)

def test_knowledge_event_timestamp_is_utc():
    e = KnowledgeEvent.create(source="cognition", knowledge_type="fact")
    assert e.created_at.tzinfo is not None
    assert e.created_at.tzinfo == timezone.utc


