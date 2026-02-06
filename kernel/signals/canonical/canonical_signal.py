# kernel/signals/canonical/canonical_signal.py

from dataclasses import dataclass
from typing import Optional
from .canonical_signal_key import CanonicalSignalKey


@dataclass(frozen=True)
class CanonicalSignal:
    signal_id: str
    key: CanonicalSignalKey
    state: str
    subject_ref: str
    temporal_anchor: str
    origin: str
    supersedes: Optional[str] = None
