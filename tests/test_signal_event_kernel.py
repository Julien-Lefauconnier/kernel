# kernel/tests/test_signal_event_kernel.py

from datetime import datetime, timezone, timezone
from dataclasses import FrozenInstanceError

from veramem_kernel.signals.signal_event import SignalEvent


def test_signal_event_creation_minimal():
    """
    Kernel invariant:
    SignalEvent must be constructible with minimal required fields.
    """
    now = datetime.now(timezone.utc)

    event = SignalEvent(
        event_id="sig-1",
        created_at=now,
        signal_type="knowledge",
        source="system",
    )

    assert event.event_id == "sig-1"
    assert event.created_at == now
    assert event.signal_type == "knowledge"
    assert event.source == "system"
    assert event.user_ref is None
    assert event.place_ref is None
    assert event.payload is None
