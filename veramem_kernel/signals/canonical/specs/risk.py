# veramem_kernel/signals/canonical/specs/risk.py

"""
Canonical Signal Specifications — Risk Domain
Universal risk-state vocabulary for cognitive systems.
"""

from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
    CanonicalSignalSpec,
)
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey


def register_risk_signals() -> None:
    specs = [
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.RISK_STATE,
                code="uncertainty_detected",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.RISK_STATE,
                code="conflict_detected",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.RISK_STATE,
                code="instability_detected",
            ),
            states_allowed=frozenset(["ACTIVE", "SUPERSEDED"]),
            subject_kinds=frozenset(["timeline:entry"]),
            origin_allowed=frozenset(["arvis"]),
            supersession_allowed=True,
        ),
        CanonicalSignalSpec(
            key=CanonicalSignalKey(
                category=CanonicalSignalCategory.RISK_STATE,
                code="early_warning_detected",
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