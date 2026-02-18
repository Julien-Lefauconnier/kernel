# tests/test_reconcile_audit_journal_kernel.py

from veramem_kernel.journals.audit.reconcile_audit_journal import ReconcileAuditJournal
from veramem_kernel.journals.timeline.timeline_reconcile import TimelineReconcileDecision
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from datetime import datetime, timezone


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:03d}",
        created_at=datetime.fromtimestamp(100 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def test_reconcile_audit_journal_append_only():
    local = TimelineSnapshot.build([_entry(i) for i in range(7)])
    remote = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])
    fork = TimelineFork.detect(local, remote)

    decision = TimelineReconcileDecision.from_fork_keep_both(fork)

    j1 = ReconcileAuditJournal()
    j2 = j1.append(decision)
    j3 = j2.append(decision)

    assert len(j1.list_events()) == 0
    assert len(j2.list_events()) == 1
    assert len(j3.list_events()) == 2
