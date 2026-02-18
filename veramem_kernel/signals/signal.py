# kernel/signals/signal.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4
import unicodedata
import inspect

@dataclass(frozen=True)
class Signal:
    """
    Kernel-level signal.

    A Signal is a raw, immutable observation entering or leaving
    the cognitive kernel.

    It:
    - carries no interpretation
    - triggers no behavior
    - contains no policy
    - is strictly declarative

    Signals are the lowest-level cognitive artifacts.
    """

    signal_id: str
    timestamp: datetime
    payload: Any

    # Optional, opaque origin reference (e.g. "http", "cli", "sensor")
    origin: Optional[str] = None

    def __post_init__(self):
        """
        Kernel invariants:
        - timestamp must always be defined
        - signals are immutable and time-bound
        """
        if self.timestamp is None:
            raise ValueError(
                "Signal.timestamp must not be None "
                "(signals are strictly time-bound)."
            )
        # --- Timestamp hardening ---
        if self.timestamp.tzinfo is None:
            raise ValueError("Signal.timestamp must be timezone-aware (UTC).")

        if self.timestamp.tzinfo.utcoffset(self.timestamp) is None:
            raise ValueError("Invalid timezone on Signal.timestamp.")

        if self.timestamp.tzinfo.utcoffset(self.timestamp).total_seconds() != 0:
            raise ValueError("Signal.timestamp must be in UTC.")

        # --- signal_id hardening ---
        if not isinstance(self.signal_id, str):
            raise ValueError("Signal.signal_id must be a string.")
        normalized = unicodedata.normalize("NFKC", self.signal_id)
        if normalized != self.signal_id:
            raise ValueError("Signal.signal_id must be normalized.")
        
        if len(self.signal_id) > 256:
            raise ValueError("Signal.signal_id too long.")
        if len(self.signal_id) < 8:
            raise ValueError("Signal.signal_id too short.")
        if not self.signal_id.isascii():
            raise ValueError("Signal.signal_id must be ASCII.")

        if any(ord(c) < 32 for c in self.signal_id):
            raise ValueError("Signal.signal_id contains control characters.")

        # --- payload safety ---
        if callable(self.payload):
            raise ValueError("Signal.payload must not be callable.")
        if inspect.isawaitable(self.payload):
            raise ValueError("Signal.payload must not be awaitable.")
        if inspect.isgenerator(self.payload):
            raise ValueError("Signal.payload must not be a generator.")
           
        # Defensive minimal determinism
        try:
            hash(self.payload)
        except Exception:
            pass  # allowed but non-hashable payload must still be inert

    # ------------------------------------------------------------------
    # Unsafe constructor (tests / adapters only)
    # ------------------------------------------------------------------
    @classmethod
    def unsafe(
        cls,
        *,
        payload: Any,
        origin: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        signal_id: Optional[str] = None,
    ) -> "Signal":
        """
        Unsafe constructor for tests or adapters.

        Bypasses strict creation guarantees.
        MUST NOT be used inside kernel logic.
        """
        return cls(
            signal_id=signal_id or str(uuid4()),
            timestamp=timestamp or datetime.now(timezone.utc),
            payload=payload,
            origin=origin,
        )
