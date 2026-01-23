# tests/test_signal_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.signals.signal import Signal
from kernel.invariants.signal.signal_invariants import (
    assert_signal_has_timestamp,
    assert_signal_is_immutable,
    assert_signal_payload_exists,
)


def make_signal(**overrides):
    data = {
        "signal_id": "s1",
        "timestamp": datetime.utcnow(),
        "payload": {"k": "v"},
        "origin": None,
    }
    data.update(overrides)
    return Signal(**data)



def test_missing_payload_is_rejected():
    signal = make_signal(payload=None)
    with pytest.raises(ValueError):
        assert_signal_payload_exists(signal)


def test_signal_is_immutable():
    signal = make_signal()
    assert_signal_is_immutable(signal)
