# veramem_kernel/signals/canonical/canonical_signal.py

from dataclasses import dataclass
from typing import Optional
from .canonical_signal_key import CanonicalSignalKey
from .canonical_signal_registry import CanonicalSignalRegistry


@dataclass(frozen=True)
class CanonicalSignal:
    signal_id: str
    key: CanonicalSignalKey
    state: str
    subject_ref: str
    temporal_anchor: str
    origin: str
    supersedes: Optional[str] = None

    def __post_init__(self) -> None:
        spec = CanonicalSignalRegistry.get(self.key)

        if self.state not in spec.states_allowed:
            raise ValueError(
                f"Invalid state '{self.state}' for canonical signal {self.key}"
            )

        if self.origin not in spec.origin_allowed:
            raise ValueError(
                f"Invalid origin '{self.origin}' for canonical signal {self.key}"
            )