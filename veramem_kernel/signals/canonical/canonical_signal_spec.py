"""
Canonical Signal Specification — Core Definition
Part of Veramem Kernel — Closed Canonical World
Version 1.1.7 — Extended with explicit allowed_states and subject_kinds validation
"""

from dataclasses import dataclass, field
from typing import FrozenSet

from .canonical_signal_key import CanonicalSignalKey


@dataclass(frozen=True)
class CanonicalSignalSpec:
    """
    Immutable specification of a canonical signal.
    
    Defines:
    - The unique key identifying the signal
    - Allowed states (finite set)
    - Allowed subject kinds (entities that can carry this signal)
    - Supersession rules
    - Allowed origins
    """
    key: CanonicalSignalKey
    
    # Explicit finite sets — extracted from private stack
    states_allowed: FrozenSet[str] = field(default_factory=frozenset)
    subject_kinds: FrozenSet[str] = field(default_factory=frozenset)
    
    # Existing fields
    supersession_allowed: bool = False
    origin_allowed: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """
        Enforce structural invariants at construction.
        """
        if not self.states_allowed:
            raise ValueError("states_allowed must not be empty (closed-world invariant)")
        
        if not self.subject_kinds:
            raise ValueError("subject_kinds must not be empty (closed-world invariant)")
        
        if not self.origin_allowed:
            raise ValueError("origin_allowed must not be empty (provenance invariant)")