# veramem_kernel/journals/timeline/timeline_head.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
import unicodedata


def _norm_ascii(s: str, *, field: str, max_len: int = 256) -> str:
    if not isinstance(s, str):
        raise ValueError(f"JournalHead.{field} must be a string.")
    s2 = unicodedata.normalize("NFKC", s).strip()
    if not s2:
        raise ValueError(f"JournalHead.{field} must be non-empty.")
    if s2 != s:
        raise ValueError(f"JournalHead.{field} must be normalized/trimmed.")
    if len(s2) > max_len:
        raise ValueError(f"JournalHead.{field} too long.")
    if not s2.isascii():
        raise ValueError(f"JournalHead.{field} must be ASCII.")
    if any(ord(c) < 32 for c in s2):
        raise ValueError(f"JournalHead.{field} contains control characters.")
    return s2


def _ensure_utc(dt: datetime, *, field: str) -> None:
    if dt is None:
        raise ValueError(f"JournalHead.{field} must not be None.")
    if dt.tzinfo is None:
        raise ValueError(f"JournalHead.{field} must be timezone-aware (UTC).")
    off = dt.tzinfo.utcoffset(dt)
    if off is None:
        raise ValueError(f"Invalid timezone on JournalHead.{field}.")
    if off.total_seconds() != 0:
        raise ValueError(f"JournalHead.{field} must be in UTC.")


def _is_hex64(s: str) -> bool:
    if len(s) != 64:
        return False
    try:
        int(s, 16)
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class JournalHead:
    """
    JournalHead — minimal, portable integrity anchor for an append-only journal.

    Intent:
    - compare two journals cheaply (sync, replication, caching)
    - verify "where the journal is at" without scanning all entries
    - remain compatible with ZK constraints (no payload)

    Fields:
    - last_hash: hash of the last entry (or snapshot tip) — typically sha256 hex (64 chars)
    - last_timestamp: timestamp of the last entry (UTC, tz-aware)
    - total_entries: monotonic count of entries included in the head
    """

    last_hash: str
    last_timestamp: datetime
    total_entries: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "last_hash", _norm_ascii(self.last_hash, field="last_hash", max_len=256)
        )

        # Enforce sha256 hex format by default.
        # (If you ever change the algo later, add an explicit algo/version field.)
        if not _is_hex64(self.last_hash):
            raise ValueError("JournalHead.last_hash must be a 64-char hex digest (sha256).")

        _ensure_utc(self.last_timestamp, field="last_timestamp")

        if not isinstance(self.total_entries, int):
            raise ValueError("JournalHead.total_entries must be an int.")
        if self.total_entries < 0:
            raise ValueError("JournalHead.total_entries must be >= 0.")

    @classmethod
    def empty(cls) -> "JournalHead":
        """
        Canonical empty head.
        Uses sha256("") as deterministic neutral element.
        """
        return cls(
            last_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            last_timestamp=datetime.fromtimestamp(0, tz=timezone.utc),
            total_entries=0,
        )


    def advance(self, *, new_hash: str, new_timestamp: datetime) -> "JournalHead":
        """
        Deterministic O(1) head progression for append-only journals.
        """
        return JournalHead(
            last_hash=new_hash,
            last_timestamp=new_timestamp,
            total_entries=self.total_entries + 1,
        )
