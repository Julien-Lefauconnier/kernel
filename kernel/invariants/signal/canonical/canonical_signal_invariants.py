# kernel/invaraints/signals/canonical/canonical_signal_invariants.py

from kernel.signals.canonical.canonical_signal import CanonicalSignal
from kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
)


def validate_canonical_signal(signal: CanonicalSignal) -> None:
    spec = CanonicalSignalRegistry.get(signal.key)

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
