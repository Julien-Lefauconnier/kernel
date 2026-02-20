# tests/test_canonical_registry.py
import pytest
from veramem_kernel.signals.canonical import (
    CanonicalSignalRegistry,
    CanonicalSignalKey,
    CanonicalSignalCategory,
)


def test_registry_auto_bootstrapped():
    """Registry doit être rempli automatiquement au import."""

    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.TEMPORAL_STATE,
        code="memory_long_projected",
    )
    spec = CanonicalSignalRegistry.get(key)
    assert spec is not None
    assert spec.key.code == "memory_long_projected"
    assert "timeline:entry" in spec.subject_kinds


def test_timeline_ghost_signal_registered():
    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.TEMPORAL_STATE,
        code="ghost_signal",
    )
    spec = CanonicalSignalRegistry.get(key)
    assert spec is not None
    assert spec.states_allowed == frozenset(["GHOST"])  


def test_registry_immutable():
    key = CanonicalSignalKey(
        category=CanonicalSignalCategory.TEMPORAL_STATE,
        code="memory_long_projected",
    )
    spec = CanonicalSignalRegistry.get(key)
    with pytest.raises(AttributeError):
        spec.key = None  