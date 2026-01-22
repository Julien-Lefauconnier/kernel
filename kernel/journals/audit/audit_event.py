# kernel/journals/audit/audit_event.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Mapping
from uuid import uuid4


@dataclass(frozen=True)
class AuditEvent:
    """
    Kernel-level audit event.

    Declares that an auditable fact occurred.
    No payload, no interpretation, no cognition.
    """

    event_id: str
    created_at: datetime

    source: str           # "action" | "timeline" | "document" | ...
    source_id: str
    event_type: str

    # Optional opaque metadata (never interpreted by the kernel)
    metadata: Optional[Mapping[str, str]] = None

    @classmethod
    def create(
        cls,
        *,
        source: str,
        source_id: str,
        event_type: str,
        created_at: Optional[datetime] = None,
        event_id: Optional[str] = None,
        metadata: Optional[Mapping[str, str]] = None,
    ) -> "AuditEvent":
        return cls(
            event_id=event_id or str(uuid4()),
            created_at=created_at or datetime.utcnow(),
            source=source,
            source_id=source_id,
            event_type=event_type,
            metadata=metadata,
        )
