# tests/test_timeline_sync_policy_kernel.py

from datetime import datetime, timezone

from veramem_kernel.common.trust_anchor import TrustAnchor
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_sync_policy import TimelineSyncPolicy
from veramem_kernel.journals.audit.reconcile_audit_journal import ReconcileAuditJournal


def _entry(
    i: int,
    ts: int | None = None,
    entry_id: str | None = None,
) -> TimelineEntry:
    t = ts if ts is not None else 100 + i
    eid = entry_id if entry_id is not None else f"entry-{i:05d}"

    return TimelineEntry(
        entry_id=eid,
        created_at=datetime.fromtimestamp(t, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )



def _snapshot(n: int) -> TimelineSnapshot:
    return TimelineSnapshot.build([_entry(i) for i in range(n)])


def test_policy_fast_path():
    local = _snapshot(5)
    remote = _snapshot(8)
    anchor = TrustAnchor(best=local.cursor())
    audit = ReconcileAuditJournal()

    r = TimelineSyncPolicy.run(
        local=local,
        remote=remote,
        anchor=anchor,
        audit=audit,
    )

    assert r.requires_decision is False
    assert r.snapshot.cursor() == remote.cursor()


def test_policy_auto_merge():
    prefix = [_entry(i) for i in range(3)]
    left = TimelineSnapshot.build(prefix + [_entry(10), _entry(11)])
    right = TimelineSnapshot.build(prefix + [_entry(20), _entry(21)])

    anchor = TrustAnchor()
    audit = ReconcileAuditJournal()

    r = TimelineSyncPolicy.run(
        local=left,
        remote=right,
        anchor=anchor,
        audit=audit,
    )

    assert r.requires_decision is False


def test_policy_requires_decision():
    prefix = [_entry(i) for i in range(3)]
    left = TimelineSnapshot.build(prefix + [_entry(10, ts=200)])
    right = TimelineSnapshot.build(prefix + [_entry(10, ts=210)])

    anchor = TrustAnchor()
    audit = ReconcileAuditJournal()

    r = TimelineSyncPolicy.run(
        local=left,
        remote=right,
        anchor=anchor,
        audit=audit,
    )

    assert r.requires_decision is True
