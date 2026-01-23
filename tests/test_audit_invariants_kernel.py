# tests/test_audit_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.journals.audit.audit_event import AuditEvent
from kernel.invariants.audit.audit_invariants import (
    assert_has_timestamp,
    assert_has_identity,
    assert_is_immutable,
)


def make_event(**kwargs):
    return AuditEvent.create(
        source="test",
        source_id="src-1",
        event_type="TEST_EVENT",
        **kwargs,
    )


def test_audit_event_has_timestamp():
    event = make_event()
    assert_has_timestamp(event)


def test_audit_event_missing_timestamp_raises():
    event = AuditEvent(
        event_id="evt-1",
        created_at=None,  # type: ignore
        source="test",
        source_id="src",
        event_type="TEST",
    )

    with pytest.raises(ValueError):
        assert_has_timestamp(event)


def test_audit_event_has_identity():
    event = make_event()
    assert_has_identity(event)


def test_audit_event_missing_identity_raises():
    event = AuditEvent(
        event_id="",
        created_at=datetime.utcnow(),
        source="test",
        source_id="src",
        event_type="TEST",
    )

    with pytest.raises(ValueError):
        assert_has_identity(event)


def test_audit_event_is_immutable():
    event = make_event()
    assert_is_immutable(event)

    with pytest.raises(Exception):
        # frozen dataclass → mutation forbidden
        event.event_type = "MUTATED"  # type: ignore
