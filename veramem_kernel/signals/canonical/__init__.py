# veramem_kernel/signals/canonical/__init__.py

"""
Canonical Signals — Closed World
Auto-bootstrap du registry au premier import.
Version 1.1.7 — Unified bootstrap
"""

from .canonical_signal import CanonicalSignal
from .canonical_signal_key import CanonicalSignalKey
from .canonical_signal_spec import CanonicalSignalSpec
from .canonical_signal_category import CanonicalSignalCategory
from .canonical_signal_registry import (
    CanonicalSignalRegistry,
    register_all_canonical_signals,
)

# Auto-registration au premier import du module
register_all_canonical_signals()

__all__ = [
    "CanonicalSignal",
    "CanonicalSignalKey",
    "CanonicalSignalSpec",
    "CanonicalSignalCategory",
    "CanonicalSignalRegistry",
    "register_all_canonical_signals",
]