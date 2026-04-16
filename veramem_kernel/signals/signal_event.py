# kernel/journals/signal/signal_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
import unicodedata


def _norm_ascii(s: str, *, field: str, max_len: int = 256) -> str:
    if not isinstance(s, str):
        raise ValueError(f"SignalEvent.{field} must be a string.")
    s2 = unicodedata.normalize("NFKC", s).strip()
    if not s2:
        raise ValueError(f"SignalEvent.{field} must be non-empty.")
    if s2 != s:
        raise ValueError(f"SignalEvent.{field} must be normalized.")
    if len(s2) > max_len:
        raise ValueError(f"SignalEvent.{field} too long.")
    if not s2.isascii():
        raise ValueError(f"SignalEvent.{field} must be ASCII.")
    if any(ord(c) < 32 for c in s2):
        raise ValueError(f"SignalEvent.{field} contains control characters.")
    return s2

@dataclass(frozen=True)
class SignalEvent:
    """
    Immutable kernel signal.

    A signal is a factual perception emitted by the system
    or an external observer. It carries no interpretation.
    """

    event_id: str
    created_at: datetime

    signal_type: str           # e.g. "knowledge", "memory_long", "normative"
    source: str                # e.g. "user", "system", "observer", "llm"

    user_ref: Optional[str] = None
    place_ref: Optional[str] = None

    payload: Optional[Dict[str, Any]] = None


    def __post_init__(self):
        if self.created_at is None:
            raise ValueError("SignalEvent.created_at must not be None.")

        if self.created_at.tzinfo is None:
            raise ValueError("SignalEvent.created_at must be timezone-aware UTC.")

        off = self.created_at.tzinfo.utcoffset(self.created_at)
        if off is None or off.total_seconds() != 0:
            raise ValueError("SignalEvent.created_at must be UTC.")

        object.__setattr__(
            self,
            "event_id",
            _norm_ascii(self.event_id, field="event_id")
        )

    @property
    def timestamp(self) -> datetime:
        return self.created_at
