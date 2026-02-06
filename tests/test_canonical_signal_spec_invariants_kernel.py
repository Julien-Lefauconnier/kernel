# tests/test_canonical_signal_spec_invariants_kernel.py

import pytest

from kernel.signals.canonical import (
    CanonicalSignalCategory,
    CanonicalSignalKey,
    CanonicalSignalSpec,
)


def test_spec_requires_states():
    with pytest.raises(ValueError):
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                CanonicalSignalCategory.COGNITIVE_STATE,
                "gap_detected",
            ),
            states_allowed=frozenset(),
            subject_kinds=frozenset({"timeline_entry"}),
            supersession_allowed=True,
            origin_allowed=frozenset({"journal"}),
        )


def test_spec_requires_subject_kinds():
    with pytest.raises(ValueError):
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                CanonicalSignalCategory.OBSERVATION_STATE,
                "observation_received",
            ),
            states_allowed=frozenset({"RECEIVED"}),
            subject_kinds=frozenset(),
            supersession_allowed=False,
            origin_allowed=frozenset({"port"}),
        )


def test_spec_requires_origin_allowed():
    with pytest.raises(ValueError):
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                CanonicalSignalCategory.KNOWLEDGE_STATE,
                "knowledge_added",
            ),
            states_allowed=frozenset({"ADDED"}),
            subject_kinds=frozenset({"knowledge_item"}),
            supersession_allowed=True,
            origin_allowed=frozenset(),
        )
