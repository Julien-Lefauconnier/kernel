# veramem_kernel/invaraints/signals/canonical/canonical_signal_invariants.py

from __future__ import annotations
import unicodedata

from veramem_kernel.signals.canonical.canonical_signal import CanonicalSignal
from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
)

def extract_subject_kind(ref: str) -> str:
    ref = (ref or "").strip()
    if not ref:
        raise ValueError("subject_ref requis")

    if ":" in ref:
        return ref.rsplit(":", 1)[0]
    if "/" in ref:
        return ref.split("/", 1)[0]
    
    # Si pas de séparateur → on considère que c'est déjà le kind pur
    return ref

def validate_canonical_signal(signal: CanonicalSignal) -> None:
    spec = CanonicalSignalRegistry.get(signal.key)
    # Expected formats: "kind:id" or "kind/id"
    subject_ref = unicodedata.normalize("NFKC", (signal.subject_ref or "")).strip()
    if not subject_ref:
        raise ValueError("CanonicalSignal.subject_ref must be defined.")

    if ":" in subject_ref:
        subject_kind = extract_subject_kind(subject_ref)
    elif "/" in subject_ref:
        subject_kind = subject_ref.split("/", 1)[0]
    else:
        raise ValueError(
            "Invalid CanonicalSignal.subject_ref format. "
            "Expected 'kind:id' or 'kind/id'."
        )
    
    if subject_kind.strip() != subject_kind:
        raise ValueError("Invalid subject kind format.")

    if subject_kind not in spec.subject_kinds:
        raise ValueError(
            f"Subject kind '{subject_kind}' not allowed for {signal.key}"
        )


    if signal.state not in spec.states_allowed:
        raise ValueError(
            f"State '{signal.state}' not allowed for {signal.key}"
        )

    if signal.origin not in spec.origin_allowed:
        raise ValueError(
            f"Origin '{signal.origin}' not allowed for {signal.key}"
        )

    if signal.supersedes is not None and not spec.supersession_allowed:
        raise ValueError(
            f"Supersession not allowed for {signal.key}"
        )
