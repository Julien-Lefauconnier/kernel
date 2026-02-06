# tests/test_canonical_signal_validation_kernel.py

import pytest

from kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalCategory,
    CanonicalSignalKey,
    CanonicalSignalSpec,
    CanonicalSignalRegistry,
)
from kernel.invariants.signal.canonical.canonical_signal_invariants import (
    validate_canonical_signal,
)



def setup_module():
    key = CanonicalSignalKey(
        CanonicalSignalCategory.TEMPORAL_STATE,
        "supersession_declared",
    )

    spec = CanonicalSignalSpec(
        key=key,
        states_allowed=frozenset({"DECLARED"}),
        subject_kinds=frozenset({"timeline_entry"}),
        supersession_allowed=True,
        origin_allowed=frozenset({"journal"}),
    )

    CanonicalSignalRegistry.register(spec)


def test_valid_canonical_signal_passes_validation():
    signal = CanonicalSignal(
        signal_id="sig-1",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.TEMPORAL_STATE,
            "supersession_declared",
        ),
        state="DECLARED",
        subject_ref="timeline:123",
        temporal_anchor="t-1",
        origin="journal",
        supersedes=None,
    )

    validate_canonical_signal(signal)


def test_invalid_state_raises():
    signal = CanonicalSignal(
        signal_id="sig-2",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.TEMPORAL_STATE,
            "supersession_declared",
        ),
        state="INVALID",
        subject_ref="timeline:123",
        temporal_anchor="t-2",
        origin="journal",
        supersedes=None,
    )

    with pytest.raises(ValueError):
        validate_canonical_signal(signal)


def test_invalid_origin_raises():
    signal = CanonicalSignal(
        signal_id="sig-3",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.TEMPORAL_STATE,
            "supersession_declared",
        ),
        state="DECLARED",
        subject_ref="timeline:123",
        temporal_anchor="t-3",
        origin="projection",
        supersedes=None,
    )

    with pytest.raises(ValueError):
        validate_canonical_signal(signal)
