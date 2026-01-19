# kernel/tests/test_signal_kernel.py

import pytest
from datetime import datetime, timedelta

from kernel.signals.signal import Signal


def test_signal_is_immutable():
    """
    Kernel invariant:
    Signal must be strictly immutable once created.
    """
    signal = Signal.unsafe(
        payload={"key": "value"},
        origin="test",
    )

    with pytest.raises(Exception):
        signal.payload = {"other": "value"}


def test_signal_timestamp_is_mandatory():
    """
    Kernel invariant:
    Signal.timestamp must never be None.
    """
    with pytest.raises(ValueError):
        Signal(
            signal_id="sig-1",
            timestamp=None,  # type: ignore
            payload={},
            origin="test",
        )


def test_signal_timestamp_is_stable():
    """
    Kernel invariant:
    Signal timestamp must remain stable and unmodified.
    """
    now = datetime.utcnow()

    signal = Signal(
        signal_id="sig-ts",
        timestamp=now,
        payload="raw",
        origin=None,
    )

    assert signal.timestamp == now
