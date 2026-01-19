# kernel/journals/signal/signal_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class SignalEvent:
    """
    Immutable kernel signal.

    A signal is a factual perception emitted by the system
    or an external observer. It carries no interpretation.
    """

    signal_id: str
    created_at: datetime

    signal_type: str           # e.g. "knowledge", "memory_long", "normative"
    source: str                # e.g. "user", "system", "observer", "llm"

    user_ref: Optional[str] = None
    place_ref: Optional[str] = None

    payload: Optional[Dict[str, Any]] = None
