# veramem_kernel/journals/audit/reconcile_audit_journal.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Tuple

from veramem_kernel.journals.audit.reconcile_audit_event import ReconcileAuditEvent
from veramem_kernel.journals.timeline.timeline_reconcile import TimelineReconcileDecision


@dataclass(frozen=True)
class ReconcileAuditJournal:
    """
    Minimal append-only journal for reconciliation decisions.
    """

    events: Tuple[ReconcileAuditEvent, ...] = ()

    def append(self, decision: TimelineReconcileDecision) -> "ReconcileAuditJournal":
        e = ReconcileAuditEvent(created_at=datetime.now(timezone.utc), decision=decision)
        return ReconcileAuditJournal(events=self.events + (e,))

    def list_events(self) -> Tuple[ReconcileAuditEvent, ...]:
        return self.events
