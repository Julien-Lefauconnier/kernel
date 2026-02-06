# kernel/signals/canonical/canonical_signal_spec.py

from dataclasses import dataclass
from typing import FrozenSet
from .canonical_signal_key import CanonicalSignalKey


@dataclass(frozen=True)
class CanonicalSignalSpec:
    key: CanonicalSignalKey
    states_allowed: FrozenSet[str]
    subject_kinds: FrozenSet[str]
    supersession_allowed: bool
    origin_allowed: FrozenSet[str]

    def __post_init__(self) -> None:
        if not self.states_allowed:
            raise ValueError("states_allowed must not be empty")
        if not self.subject_kinds:
            raise ValueError("subject_kinds must not be empty")
        if not self.origin_allowed:
            raise ValueError("origin_allowed must not be empty")
