# tests/test_audit_journal_kernel.py

import pytest

from kernel.journals.audit.audit_event import AuditEvent
from kernel.journals.audit.audit_journal import AuditJournal


def test_audit_journal_starts_empty():
    journal = AuditJournal()
    assert list(journal.iter_events()) == []


def test_audit_journal_append_event():
    journal = AuditJournal()
    event = AuditEvent.create(
        source="action",
        source_id="a1",
        event_type="created",
    )

    journal.append(event)

    events = list(journal.iter_events())
    assert len(events) == 1
    assert events[0] is event


def test_audit_journal_preserves_order():
    journal = AuditJournal()

    e1 = AuditEvent.create(source="action", source_id="a1", event_type="created")
    e2 = AuditEvent.create(source="action", source_id="a1", event_type="validated")

    journal.append(e1)
    journal.append(e2)

    events = list(journal.iter_events())
    assert events == [e1, e2]


def test_audit_journal_is_append_only():
    journal = AuditJournal()
    event = AuditEvent.create(
        source="timeline",
        source_id="t1",
        event_type="appended",
    )

    journal.append(event)
    events = journal.iter_events()

    assert isinstance(events, tuple)

    with pytest.raises(AttributeError):
        events.pop()

    with pytest.raises(TypeError):
        events[0] = event


def test_audit_journal_rejects_invalid_event():
    journal = AuditJournal()

    with pytest.raises(TypeError):
        journal.append("not-an-audit-event")
