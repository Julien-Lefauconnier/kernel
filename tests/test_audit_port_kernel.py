# tests/test_audit_port_kernel.py

import pytest

from kernel.ports.audit_port import append_audit
from kernel.journals.audit import get_audit_journal
from kernel.journals.audit.audit_event import AuditEvent


def test_append_audit_port_appends_event():
    journal = get_audit_journal()
    journal._events.clear()

    event = AuditEvent.create(
        source="test",
        source_id="123",
        event_type="TEST_EVENT",
    )

    append_audit(event)

    events = list(journal.iter_events())
    assert len(events) == 1
    assert events[0] == event


def test_append_audit_port_rejects_invalid_type():
    with pytest.raises(TypeError):
        append_audit("not an audit event")
