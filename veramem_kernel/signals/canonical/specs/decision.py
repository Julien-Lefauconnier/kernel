# veramem_kernel/signals/canonical/specs/decision.py

"""
Canonical Signal Specifications — Decision Domain
Universal decision-state vocabulary for cognitive systems.
"""

from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
    CanonicalSignalSpec,
)
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey


def register_decision_signals() -> None:
    specs = [
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.DECISION_STATE,
                code="decision_emitted",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.DECISION_STATE,
                code="decision_actionable",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.DECISION_STATE,
                code="decision_memory_related",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.DECISION_STATE,
                code="decision_meta",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.DECISION_STATE,
                code="decision_informational",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
    ]

    for spec in specs:
        if not CanonicalSignalRegistry.has(spec.key):
            CanonicalSignalRegistry.register(spec)