# tests/test_canonical_signal_registry_kernel.py

import pytest

from veramem_kernel.signals.canonical import (
    CanonicalSignalCategory,
    CanonicalSignalKey,
    CanonicalSignalSpec,
    CanonicalSignalRegistry,
)
from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
    register_all_canonical_signals,
)


def test_register_and_get_canonical_signal_spec():
    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.COGNITIVE_STATE,
        code="conflict_detected",
    )

    spec = CanonicalSignalSpec(
        key=key,
        states_allowed=frozenset({"DETECTED"}),
        subject_kinds=frozenset({"timeline_entry"}),
        supersession_allowed=True,
        origin_allowed=frozenset({"journal"}),
    )

    CanonicalSignalRegistry.register(spec)

    retrieved = CanonicalSignalRegistry.get(key)
    assert retrieved is spec


def test_duplicate_canonical_signal_key_raises():
    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.ACCESS_STATE,
        code="access_denied",
    )

    spec = CanonicalSignalSpec(
        key=key,
        states_allowed=frozenset({"DENIED"}),
        subject_kinds=frozenset({"access_request"}),
        supersession_allowed=False,
        origin_allowed=frozenset({"invariant"}),
    )

    CanonicalSignalRegistry.register(spec)

    with pytest.raises(ValueError):
        CanonicalSignalRegistry.register(spec)



def test_new_decision_signals_are_registered():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.DECISION_STATE,
            "decision_emitted",
        )
    )
    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.DECISION_STATE,
            "decision_actionable",
        )
    )


def test_new_risk_signals_are_registered():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.RISK_STATE,
            "uncertainty_detected",
        )
    )
    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.RISK_STATE,
            "instability_detected",
        )
    )


def test_new_validation_signals_are_registered():
    CanonicalSignalRegistry._clear_for_tests()
    register_all_canonical_signals()

    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.VALIDATION_STATE,
            "gate_allow",
        )
    )
    assert CanonicalSignalRegistry.has(
        CanonicalSignalKey(
            CanonicalSignalCategory.VALIDATION_STATE,
            "projection_invalid",
        )
    )