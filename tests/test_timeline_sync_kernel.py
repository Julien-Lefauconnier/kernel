# tests/test_timeline_sync_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.common.trust_anchor import TrustAnchor, RollbackDetected
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_sync import (
    TimelineSync,
    TimelineSyncKind,
)


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


def _snapshot(n: int) -> TimelineSnapshot:
    return TimelineSnapshot.build([_entry(i) for i in range(n)])


def test_sync_identical():
    a = _snapshot(5)
    b = _snapshot(5)
    anchor = TrustAnchor()

    r = TimelineSync.sync(local=a, remote=b, anchor=anchor)

    assert r.kind == TimelineSyncKind.IDENTICAL
    assert r.delta is None


def test_sync_remote_extends_local_produces_delta_and_applies():
    local = _snapshot(5)
    remote = _snapshot(8)
    anchor = TrustAnchor(best=local.cursor())

    r = TimelineSync.sync(local=local, remote=remote, anchor=anchor)

    assert r.kind == TimelineSyncKind.LOCAL_NEEDS_REMOTE
    assert r.delta is not None

    updated, new_anchor = TimelineSync.apply_local_update(local=local, result=r, anchor=anchor)

    assert updated.cursor() == remote.cursor()
    assert new_anchor.best == remote.cursor()


def test_sync_local_extends_remote_produces_delta_for_remote():
    local = _snapshot(8)
    remote = _snapshot(5)
    anchor = TrustAnchor(best=remote.cursor())

    r = TimelineSync.sync(local=local, remote=remote, anchor=anchor)

    assert r.kind == TimelineSyncKind.REMOTE_NEEDS_LOCAL
    assert r.delta is not None

    # delta should rebuild local when applied to remote base
    rebuilt = r.delta.apply_to(remote)
    assert rebuilt.cursor() == local.cursor()


def test_sync_detects_fork():
    left = TimelineSnapshot.build([_entry(i) for i in range(7)])
    right = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])
    anchor = TrustAnchor()

    r = TimelineSync.sync(local=left, remote=right, anchor=anchor)

    assert r.kind == TimelineSyncKind.FORK
    assert r.delta is None
    assert r.fork.is_fork() is True


def test_sync_rejects_rollback_against_anchor():
    anchor = TrustAnchor(best=_snapshot(10).cursor())

    local = _snapshot(5)
    remote = _snapshot(5)

    with pytest.raises(RollbackDetected):
        _ = TimelineSync.sync(local=local, remote=remote, anchor=anchor)
