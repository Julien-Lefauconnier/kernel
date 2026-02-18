# tests/test_signal_invariants_kernel.py

import pytest
from datetime import datetime, timezone, timezone
from uuid import uuid4

from veramem_kernel.signals.signal import Signal
from veramem_kernel.invariants.signal.signal_invariants import (
    assert_signal_has_timestamp,
    assert_signal_is_immutable,
    assert_signal_payload_exists,
)


def make_signal(**overrides):
    from uuid import uuid4

    data = {
        "signal_id": f"sig-{uuid4()}",
        "timestamp": datetime.now(timezone.utc),
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
