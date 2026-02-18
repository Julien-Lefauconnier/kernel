# tests/test_canonical_signal_immutability_kernel.py

import pytest
from veramem_kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalKey,
    CanonicalSignalCategory,
    CanonicalSignalSpec,
    CanonicalSignalRegistry,
)

def _register_memory_long_projected():
    CanonicalSignalRegistry._clear_for_tests()

    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.TEMPORAL_STATE,
        code="memory_long_projected",
    )

    spec = CanonicalSignalSpec(
        key=key,
        states_allowed=frozenset({"PROJECTED"}),
        subject_kinds=frozenset({"timeline_entry"}),
        supersession_allowed=False,
        origin_allowed=frozenset({"timeline"}),
    )

    CanonicalSignalRegistry.register(spec)

def make_signal():
    _register_memory_long_projected()

    return CanonicalSignal(
        signal_id="sig-1",
        key=CanonicalSignalKey(
            category=CanonicalSignalCategory.TEMPORAL_STATE,
            code="memory_long_projected",
        ),
        state="PROJECTED",
        subject_ref="timeline_entry:1",
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


def test_canonical_signal_is_hashable_in_set():
    signal = make_signal()
    s = {signal}
    assert signal in s
