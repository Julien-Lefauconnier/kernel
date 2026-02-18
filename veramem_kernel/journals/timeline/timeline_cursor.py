# kernel/journals/timeline/timeline_cursor.py
"""
TimelineCursor is intentionally NOT orderable.

Reason:
Distributed clock skew makes timestamp ordering unsafe.
Cursors are equality-only.
Causal ordering is handled at entry level via Lamport clocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional, Dict

from veramem_kernel.common.canonical_encoding import encode_message, decode_message, TLV


@dataclass(frozen=True)
class TimelineCursor:
    """
    Immutable, comparable cursor representing a position
    in the timeline.

    Kernel-level temporal + cryptographic primitive:
    - pure value object
    - deterministic
    - sync-friendly
    """

    # Informational only: MUST NOT be used for ordering or identity. Used only for human inspection and debugging.
    timestamp: Optional[datetime]
    #  distributed sync primitives
    head: Optional[str] = None
    total_entries: int = 0

    # IMPORTANT: no global ordering in distributed systems.
    # Remove __lt__ / ordering operators entirely (if any existed).

    # --------------------------------------------------
    # Invariants
    # --------------------------------------------------
    def __post_init__(self):
        if self.timestamp is None:
            raise ValueError("TimelineCursor.timestamp must not be None")

        if self.timestamp.tzinfo is None:
            raise ValueError("TimelineCursor.timestamp must be timezone-aware")

        off = self.timestamp.tzinfo.utcoffset(self.timestamp)
        if off is None:
            raise ValueError("Invalid timezone on TimelineCursor.timestamp")
        if off != timedelta(0):
            raise ValueError("TimelineCursor.timestamp must be UTC")

        # ---- distributed invariants ----
        if self.total_entries < 0:
            raise ValueError("TimelineCursor.total_entries must be >= 0")

        if self.head is None:
            if self.total_entries != 0:
                raise ValueError("Empty cursor must have total_entries=0")
        else:
            if not isinstance(self.head, str):
                raise ValueError("TimelineCursor.head must be string")

            if len(self.head) != 64:
                raise ValueError("TimelineCursor.head must be sha256 hex")

            if any(c not in "0123456789abcdef" for c in self.head):
                raise ValueError("TimelineCursor.head must be lowercase hex")

    # --------------------------------------------------
    # Comparisons
    # --------------------------------------------------
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimelineCursor):
            return False
        # Distributed identity: timestamp is NOT part of cursor identity.
        return (self.head, self.total_entries) == (other.head, other.total_entries)

    def __hash__(self) -> int:
        # Keep hash aligned with __eq__ for safe dict/set usage.
        return hash((self.head, self.total_entries))
    
    # --------------------------------------------------
    # Serialization
    # --------------------------------------------------
    def to_dict(self) -> dict:
        payload = {
            "timestamp": self.timestamp.isoformat(),
        }

        # backward compatibility
        if self.head is not None:
            payload["head"] = self.head
            payload["total_entries"] = self.total_entries

        return payload

    # --------------------------------------------------
    # TLV serialization
    # --------------------------------------------------
    def to_bytes(self) -> bytes:
        # timestamp is mandatory and already validated in __post_init__
        ts = self.timestamp.isoformat().encode("ascii")
        head = (self.head or "").encode("ascii")

        return encode_message(
            domain=b"veramem.timeline.cursor.v1",
            fields=[
                TLV(1, b"\x01"),
                TLV(2, ts),
                TLV(3, head),
                TLV(4, self.total_entries.to_bytes(8, "big")),
            ],
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineCursor":
        dom, tlvs = decode_message(raw)

        if dom != b"veramem.timeline.cursor.v1":
            raise ValueError("invalid cursor domain")

        fields = {t.tag: t.value for t in tlvs}

        if 1 not in fields:
            raise ValueError("missing cursor wire version")
        
        if fields[1] != b"\x01":
            raise ValueError("unsupported version")

        try:
            ts_raw = fields[2]
            head_raw = fields[3]
            total_raw = fields[4]
        except KeyError as e:
            raise ValueError(f"missing cursor field: {e}") from e
        
        if not ts_raw.isascii():
            raise ValueError("timestamp must be ASCII")

        try:
            head = head_raw.decode("ascii") or None
        except Exception:
            raise ValueError("invalid head encoding")
        
        if head is not None:
            if len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
                raise ValueError("invalid head")
            
        # --- strict timestamp decoding ---
        
        try:
            ts = datetime.fromisoformat(ts_raw.decode("ascii"))
        except Exception:
            raise ValueError("invalid timestamp")
        if ts.tzinfo is None or ts.tzinfo.utcoffset(ts) != timedelta(0):
            raise ValueError("cursor timestamp must be UTC")
        if len(ts_raw) > 128:
            raise ValueError("timestamp too long")

        # --- head and total ---
        total = int.from_bytes(total_raw, "big")

        return cls(timestamp=ts, head=head, total_entries=total)


    @classmethod
    def from_dict(cls, payload: dict) -> "TimelineCursor":
        try:
            ts = datetime.fromisoformat(payload["timestamp"])
        except Exception as exc:
            raise ValueError("Invalid TimelineCursor payload") from exc

        if ts.tzinfo is None:
            raise ValueError("TimelineCursor timestamp must be timezone-aware")

        off = ts.tzinfo.utcoffset(ts)
        if off is None:
            raise ValueError("Invalid TimelineCursor timezone")
        if off != timedelta(0):
            raise ValueError("TimelineCursor timestamp must be UTC")

        return cls(
            timestamp=ts,
            head=payload.get("head"),
            total_entries=payload.get("total_entries", 0),
        )


    # --------------------------------------------------
    # Factories
    # --------------------------------------------------
    @classmethod
    def now(cls) -> "TimelineCursor":
        return cls(timestamp=datetime.now(timezone.utc))
