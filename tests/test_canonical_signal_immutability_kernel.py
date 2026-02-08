# tests/test_canonical_signal_immutability_kernel.py

import pytest
from kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalKey,
    CanonicalSignalCategory,
)


def make_signal():
    return CanonicalSignal(
        signal_id="sig-1",
        key=CanonicalSignalKey(
            category=CanonicalSignalCategory.TEMPORAL_STATE,
            code="memory_long_projected",
        ),
        state="PROJECTED",
        subject_ref="timeline:entry:1",
        temporal_anchor="t-1",
        origin="timeline",
        supersedes=None,
    )


def test_canonical_signal_is_immutable():
    signal = make_signal()

    with pytest.raises(Exception):
        signal.state = "INVALID"

    with pytest.raises(Exception):
        signal.origin = "other"

    with pytest.raises(Exception):
        signal.supersedes = "x"


def test_canonical_signal_hash_is_stable():
    signal = make_signal()
    h1 = hash(signal)
    h2 = hash(signal)
    assert h1 == h2
