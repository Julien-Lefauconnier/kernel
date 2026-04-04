# veramem_kernel/signals/canonical/specs/validation.py

"""
Canonical Signal Specifications — Validation Domain
Universal validation / gate vocabulary for cognitive systems.
"""

from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
    CanonicalSignalSpec,
)
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey


def register_validation_signals() -> None:
    specs = [
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.VALIDATION_STATE,
                code="gate_allow",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.VALIDATION_STATE,
                code="gate_require_confirmation",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.VALIDATION_STATE,
                code="gate_abstain",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.VALIDATION_STATE,
                code="projection_valid",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.VALIDATION_STATE,
                code="projection_invalid",
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