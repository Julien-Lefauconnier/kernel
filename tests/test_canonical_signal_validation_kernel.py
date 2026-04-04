# tests/test_canonical_signal_validation_kernel.py

import pytest

from veramem_kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalCategory,
    CanonicalSignalKey,
    CanonicalSignalSpec,
    CanonicalSignalRegistry,
)
from veramem_kernel.invariants.signal.canonical.canonical_signal_invariants import (
    validate_canonical_signal,
)
from veramem_kernel.signals.canonical.canonical_signal import CanonicalSignal
from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
    register_all_canonical_signals,
)
from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.invariants.signal.canonical.canonical_signal_invariants import (
    validate_canonical_signal,
)


def _register_supersession_declared():
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
    CanonicalSignalRegistry._clear_for_tests()
    _register_supersession_declared()

    signal = CanonicalSignal(
        signal_id="sig-1",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.TEMPORAL_STATE,
            "supersession_declared",
        ),
        state="DECLARED",
        subject_ref="timeline_entry:123",
        temporal_anchor="t-1",
        origin="journal",
        supersedes=None,
    )

    validate_canonical_signal(signal)



def test_invalid_state_raises():
    CanonicalSignalRegistry._clear_for_tests()
    _register_supersession_declared()

    with pytest.raises(ValueError):
        CanonicalSignal(
            signal_id="sig-2",
            key=CanonicalSignalKey(
                CanonicalSignalCategory.TEMPORAL_STATE,
                "supersession_declared",
            ),
            state="INVALID",
            subject_ref="timeline_entry:123",
            temporal_anchor="t-2",
            origin="journal",
            supersedes=None,
        )



def test_invalid_origin_raises():
    CanonicalSignalRegistry._clear_for_tests()
    _register_supersession_declared()

    with pytest.raises(ValueError):
        CanonicalSignal(
            signal_id="sig-3",
            key=CanonicalSignalKey(
                CanonicalSignalCategory.TEMPORAL_STATE,
                "supersession_declared",
            ),
            state="DECLARED",
            subject_ref="timeline_entry:123",
            temporal_anchor="t-3",
            origin="projection",
            supersedes=None,
        )

def test_decision_actionable_signal_is_valid():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    signal = CanonicalSignal(
        signal_id="sig-decision-1",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.DECISION_STATE,
            "decision_actionable",
        ),
        state="ACTIVE",
        subject_ref="timeline:entry:123",
        temporal_anchor="t-1",
        origin="arvis",
        supersedes=None,
    )

    validate_canonical_signal(signal)


def test_gate_allow_signal_is_valid():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    signal = CanonicalSignal(
        signal_id="sig-gate-1",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.VALIDATION_STATE,
            "gate_allow",
        ),
        state="ACTIVE",
        subject_ref="timeline:entry:123",
        temporal_anchor="t-2",
        origin="arvis",
        supersedes=None,
    )

    validate_canonical_signal(signal)


def test_uncertainty_detected_signal_is_valid():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    signal = CanonicalSignal(
        signal_id="sig-risk-1",
        key=CanonicalSignalKey(
            CanonicalSignalCategory.RISK_STATE,
            "uncertainty_detected",
        ),
        state="ACTIVE",
        subject_ref="timeline:entry:123",
        temporal_anchor="t-3",
        origin="arvis",
        supersedes=None,
    )

    validate_canonical_signal(signal)


def test_invalid_origin_for_decision_signal_raises():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    with pytest.raises(ValueError):
        CanonicalSignal(
            signal_id="sig-bad-origin",
            key=CanonicalSignalKey(
                CanonicalSignalCategory.DECISION_STATE,
                "decision_emitted",
            ),
            state="ACTIVE",
            subject_ref="timeline:entry:123",
            temporal_anchor="t-4",
            origin="timeline",
            supersedes=None,
        )