# veramem_kernel/journals/timeline/timeline_sync_policy.py

from __future__ import annotations

from dataclasses import dataclass

from veramem_kernel.common.trust_anchor import TrustAnchor
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_sync import TimelineSync, TimelineSyncKind
from veramem_kernel.journals.timeline.timeline_merge import TimelineMerge
from veramem_kernel.journals.timeline.timeline_reconcile import (
    TimelineReconcileDecision,
    TimelineReconcile,
)
from veramem_kernel.journals.audit.reconcile_audit_journal import ReconcileAuditJournal


class TimelineSyncPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class TimelineSyncPolicyResult:
    snapshot: TimelineSnapshot
    anchor: TrustAnchor
    audit: ReconcileAuditJournal
    requires_decision: bool


class TimelineSyncPolicy:
    """
    Deterministic orchestration of timeline synchronization.

    Kernel-grade:
    - no I/O
    - no randomness
    - audit-ready
    """

    @staticmethod
    def run(
        *,
        local: TimelineSnapshot,
        remote: TimelineSnapshot,
        anchor: TrustAnchor,
        audit: ReconcileAuditJournal,
    ) -> TimelineSyncPolicyResult:

        # Step 1 — sync classification
        sync = TimelineSync.sync(local=local, remote=remote, anchor=anchor)

        # Step 2 — identical
        if sync.kind == TimelineSyncKind.IDENTICAL:
            return TimelineSyncPolicyResult(
                snapshot=local,
                anchor=anchor,
                audit=audit,
                requires_decision=False,
            )

        # Step 3 — fast path delta
        if sync.kind == TimelineSyncKind.LOCAL_NEEDS_REMOTE:
            updated, new_anchor = TimelineSync.apply_local_update(
                local=local, result=sync, anchor=anchor
            )
            return TimelineSyncPolicyResult(
                snapshot=updated,
                anchor=new_anchor,
                audit=audit,
                requires_decision=False,
            )

        # Step 4 — local ahead: no change
        if sync.kind == TimelineSyncKind.REMOTE_NEEDS_LOCAL:
            return TimelineSyncPolicyResult(
                snapshot=local,
                anchor=anchor,
                audit=audit,
                requires_decision=False,
            )

        # Step 5 — fork
        fork = sync.fork

        # Step 6 — try auto merge
        merge = TimelineMerge.try_merge(
            fork=fork,
            local=local,
            remote=remote,
        )

        if merge.kind == "merged":
            merged = merge.merged
            new_anchor = anchor.advance(merged.cursor())

            return TimelineSyncPolicyResult(
                snapshot=merged,
                anchor=new_anchor,
                audit=audit,
                requires_decision=False,
            )

        # Step 7 — require decision
        return TimelineSyncPolicyResult(
            snapshot=local,
            anchor=anchor,
            audit=audit,
            requires_decision=True,
        )

    @staticmethod
    def apply_decision(
        *,
        fork,
        local: TimelineSnapshot,
        remote: TimelineSnapshot,
        decision: TimelineReconcileDecision,
        anchor: TrustAnchor,
        audit: ReconcileAuditJournal,
    ) -> TimelineSyncPolicyResult:

        result = TimelineReconcile.apply(
            fork=fork,
            local=local,
            remote=remote,
            decision=decision,
        )

        new_anchor = anchor.advance(result.primary.cursor())
        new_audit = audit.append(decision)

        return TimelineSyncPolicyResult(
            snapshot=result.primary,
            anchor=new_anchor,
            audit=new_audit,
            requires_decision=False,
        )
