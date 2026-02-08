# kernel/signals/lineage/signal_lineage_patch.py

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional

from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey


class SignalLineagePatchType(Enum):
    ADD = auto()
    REMOVE = auto()
    MOVE = auto()
    REWIRE_PARENTS = auto()


@dataclass(frozen=True)
class SignalLineagePatch:
    """
    Immutable, atomic lineage mutation instruction.
    """

    type: SignalLineagePatchType
    key: CanonicalSignalKey
    parents: Optional[Tuple[CanonicalSignalKey, ...]] = None

    def __init__(
        self,
        type: SignalLineagePatchType,
        key: CanonicalSignalKey | None = None,
        parents: Optional[Tuple[CanonicalSignalKey, ...]] = None,
        *,
        signal: CanonicalSignalKey | None = None,
    ):
        # Resolve alias
        resolved_key = key if key is not None else signal

        if resolved_key is None:
            raise TypeError("SignalLineagePatch requires `key` or `signal`")

        object.__setattr__(self, "type", type)
        object.__setattr__(self, "key", resolved_key)
        object.__setattr__(self, "parents", parents)
