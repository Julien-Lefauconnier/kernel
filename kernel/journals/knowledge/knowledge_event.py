# kernel/journals/knowledge/knowledge_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4


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
            created_at=created_at or datetime.utcnow(),
            source=source,
            knowledge_type=knowledge_type,
            user_ref=user_ref,
            place_ref=place_ref,
        )
