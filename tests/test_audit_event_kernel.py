# tests/test_audit_event_kernel.py

from datetime import datetime
import pytest

from kernel.journals.audit.audit_event import AuditEvent


def test_audit_event_is_immutable():
    event = AuditEvent.create(
        source="action",
        source_id="a1",
        event_type="created",
    )

    with pytest.raises(Exception):
        event.source = "other"


def test_audit_event_has_auto_id_and_timestamp():
    event = AuditEvent.create(
        source="timeline",
        source_id="t1",
        event_type="appended",
    )

    assert event.event_id is not None
    assert isinstance(event.event_id, str)
    assert event.created_at is not None
    assert isinstance(event.created_at, datetime)


def test_audit_event_preserves_explicit_values():
    now = datetime(2024, 1, 1)

    event = AuditEvent.create(
        event_id="audit-123",
        created_at=now,
        source="document",
        source_id="doc-9",
        event_type="read",
        metadata={"scope": "preview"},
    )

    assert event.event_id == "audit-123"
    assert event.created_at == now
    assert event.source == "document"
    assert event.source_id == "doc-9"
    assert event.event_type == "read"
    assert event.metadata == {"scope": "preview"}


def test_audit_event_has_no_payload_or_snapshot():
    event = AuditEvent.create(
        source="action",
        source_id="a1",
        event_type="validated",
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
