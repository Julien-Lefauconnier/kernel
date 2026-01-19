# kernel/tests/test_signal_event_kernel.py

from datetime import datetime
from dataclasses import FrozenInstanceError

from kernel.signals.signal_event import SignalEvent


def test_signal_event_creation_minimal():
    """
    Kernel invariant:
    SignalEvent must be constructible with minimal required fields.
    """
    now = datetime.utcnow()

    event = SignalEvent(
        signal_id="sig-1",
        created_at=now,
        signal_type="knowledge",
        source="system",
    )

    assert event.signal_id == "sig-1"
    assert event.created_at == now
    assert event.signal_type == "knowledge"
    assert event.source == "system"
    assert event.user_ref is None
    assert event.place_ref is None
    assert event.payload is None
