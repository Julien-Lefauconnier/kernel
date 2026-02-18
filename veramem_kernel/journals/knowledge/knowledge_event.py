# veramem_kernel/journals/knowledge/knowledge_event.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
import unicodedata


def _norm_ascii(s: str, *, field: str, max_len: int = 128) -> str:
    if not isinstance(s, str):
        raise ValueError(f"KnowledgeEvent.{field} must be a string.")
    s2 = unicodedata.normalize("NFKC", s).strip()
    if not s2:
        raise ValueError(f"KnowledgeEvent.{field} must be non-empty.")
    if s2 != s:
        raise ValueError(f"KnowledgeEvent.{field} must be normalized/trimmed.")
    if len(s2) > max_len:
        raise ValueError(f"KnowledgeEvent.{field} too long.")
    if not s2.isascii():
        raise ValueError(f"KnowledgeEvent.{field} must be ASCII.")
    if any(ord(c) < 32 for c in s2):
        raise ValueError(f"KnowledgeEvent.{field} contains control characters.")
    return s2


def _norm_optional_ref(s: Optional[str], *, field: str, max_len: int = 256) -> Optional[str]:
    if s is None:
        return None
    if not isinstance(s, str):
        raise ValueError(f"KnowledgeEvent.{field} must be a string.")
    s2 = unicodedata.normalize("NFKC", s).strip()
    if not s2:
        return None
    if s2 != s:
        raise ValueError(f"KnowledgeEvent.{field} must be normalized/trimmed.")
    if len(s2) > max_len:
        raise ValueError(f"KnowledgeEvent.{field} too long.")
    if not s2.isascii():
        raise ValueError(f"KnowledgeEvent.{field} must be ASCII.")
    if any(ord(c) < 32 for c in s2):
        raise ValueError(f"KnowledgeEvent.{field} contains control characters.")
    return s2


@dataclass(frozen=True)
class KnowledgeEvent:
    """
    Kernel-level knowledge event.
    Declares that a knowledge artifact exists at a given time.
    No payload, no interpretation.
    """

    event_id: str
    created_at: datetime

    # Declarative metadata (opaque)
    source: str
    knowledge_type: str

    # Optional references (never dereferenced)
    user_ref: Optional[str] = None
    place_ref: Optional[str] = None

    def __post_init__(self) -> None:
        # --- created_at hardening (UTC tz-aware) ---
        if self.created_at is None:
            raise ValueError("KnowledgeEvent.created_at must not be None.")
        if self.created_at.tzinfo is None:
            raise ValueError("KnowledgeEvent.created_at must be timezone-aware (UTC).")
        off = self.created_at.tzinfo.utcoffset(self.created_at)
        if off is None:
            raise ValueError("Invalid timezone on KnowledgeEvent.created_at.")
        if off.total_seconds() != 0:
            raise ValueError("KnowledgeEvent.created_at must be in UTC.")

        # --- ids / fields hardening ---
        object.__setattr__(self, "event_id", _norm_ascii(self.event_id, field="event_id", max_len=256))
        object.__setattr__(self, "source", _norm_ascii(self.source, field="source", max_len=128))
        object.__setattr__(self, "knowledge_type", _norm_ascii(self.knowledge_type, field="knowledge_type", max_len=128))


        object.__setattr__(self, "user_ref", _norm_optional_ref(self.user_ref, field="user_ref"))
        object.__setattr__(self, "place_ref", _norm_optional_ref(self.place_ref, field="place_ref"))


    @classmethod
    def create(
        cls,
        *,
        source: str,
        knowledge_type: str,
        user_ref: Optional[str] = None,
        place_ref: Optional[str] = None,
        created_at: Optional[datetime] = None,
        event_id: Optional[str] = None,
    ) -> "KnowledgeEvent":
        return cls(
            event_id=event_id or str(uuid4()),
            created_at=created_at or datetime.now(timezone.utc),
            source=source,
            knowledge_type=knowledge_type,
            user_ref=user_ref,
            place_ref=place_ref,
        )
