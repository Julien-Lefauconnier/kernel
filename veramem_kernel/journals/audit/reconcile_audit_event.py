# veramem_kernel/journals/audit/reconcile_audit_event.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_reconcile import (
    TimelineReconcileDecision,
)


@dataclass(frozen=True)
class ReconcileAuditEvent:
    """
    Append-only audit event recording a fork reconciliation decision.
    """

    created_at: datetime
    decision: TimelineReconcileDecision

    def __post_init__(self) -> None:
        if self.created_at.tzinfo != timezone.utc:
            raise ValueError("ReconcileAuditEvent.created_at must be UTC")
