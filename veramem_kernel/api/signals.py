# veramem_kernel/api/signals.py
"""
Signals public API.

Includes:
- Signal core types
- Canonical signals (registry/spec/key/category)
- Signal lineage (diff/patch/view/projector/resolver)
"""

from ..signals.signal import Signal
from ..signals.signal_event import SignalEvent
from ..signals.signal_journal import SignalJournal

from ..signals.canonical.canonical_signal import CanonicalSignal
from ..signals.canonical.canonical_signal_registry import CanonicalSignalRegistry
from ..signals.canonical.canonical_signal_spec import CanonicalSignalSpec
from ..signals.canonical.canonical_signal_key import CanonicalSignalKey
from ..signals.canonical.canonical_signal_category import CanonicalSignalCategory


from ..signals.lineage.signal_lineage_patch import SignalLineagePatch
from ..signals.lineage.signal_lineage_view import SignalLineageView
from ..signals.lineage.signal_lineage_node import SignalLineageNode
from ..signals.lineage.signal_lineage_errors import SignalLineageError

__all__ = [
    "Signal",
    "SignalEvent",
    "SignalJournal",
    "CanonicalSignal",
    "CanonicalSignalRegistry",
    "CanonicalSignalSpec",
    "CanonicalSignalKey",
    "CanonicalSignalCategory",
    "SignalLineagePatch",
    "SignalLineageView",
    "SignalLineageNode",
    "SignalLineageError",
]
