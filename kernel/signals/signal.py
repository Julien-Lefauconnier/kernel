# kernel/signals/signal.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4


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
            timestamp=timestamp or datetime.utcnow(),
            payload=payload,
            origin=origin,
        )
