# kernel/signals/lineage/signal_lineage_node.py

from dataclasses import dataclass
from typing import Tuple, Optional

from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.journals.timeline.timeline_cursor import TimelineCursor


@dataclass(frozen=True)
class SignalLineageNode:
    signal_key: CanonicalSignalKey
    emitted_at: TimelineCursor
    parents: Tuple[CanonicalSignalKey, ...]
    supersedes: Optional[CanonicalSignalKey] = None

    def __init__(
        self,
        signal_key: CanonicalSignalKey | None = None,
        emitted_at: TimelineCursor | None = None,
        parents: Tuple[CanonicalSignalKey, ...] = (),
        supersedes: Optional[CanonicalSignalKey] = None,
        *,
        key: CanonicalSignalKey | None = None,
    ):
        resolved_key = signal_key if signal_key is not None else key
        if resolved_key is None:
            raise TypeError("SignalLineageNode requires `signal_key` or `key`")

        if emitted_at is None:
            raise TypeError("SignalLineageNode requires `emitted_at`")

        object.__setattr__(self, "signal_key", resolved_key)
        object.__setattr__(self, "emitted_at", emitted_at)
        object.__setattr__(self, "parents", parents)
        object.__setattr__(self, "supersedes", supersedes)
