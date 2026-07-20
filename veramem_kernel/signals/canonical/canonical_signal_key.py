# veramem_kernel/signals/canonical/canonical_signal_key.py

from dataclasses import dataclass
from .canonical_signal_category import CanonicalSignalCategory


@dataclass(frozen=True)
class CanonicalSignalKey:
    category: CanonicalSignalCategory
    code: str  # snake_case, stable, non-métier

    def __post_init__(self) -> None:
        if not self.code or not self.code.isidentifier():
            raise ValueError(f"Invalid canonical signal code: {self.code}")
