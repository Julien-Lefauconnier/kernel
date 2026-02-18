# tests/test_timeline_reconcile_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_reconcile import (
    TimelineReconcile,
    TimelineReconcileDecision,
    ReconcileDecisionKind,
    TimelineReconcileError,
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


def test_reconcile_keep_local():
    local = TimelineSnapshot.build([_entry(i) for i in range(7)])
    remote = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])

    fork = TimelineFork.detect(local, remote)

    decision = TimelineReconcileDecision.from_fork_keep_local(fork)
    out = TimelineReconcile.apply(fork=fork, local=local, remote=remote, decision=decision)

    assert out.kind == ReconcileDecisionKind.KEEP_LOCAL
    assert out.primary.cursor() == local.cursor()
    assert out.secondary is None


def test_reconcile_keep_remote():
    local = TimelineSnapshot.build([_entry(i) for i in range(7)])
    remote = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])

    fork = TimelineFork.detect(local, remote)

    decision = TimelineReconcileDecision.from_fork_keep_remote(fork)
    out = TimelineReconcile.apply(fork=fork, local=local, remote=remote, decision=decision)

    assert out.kind == ReconcileDecisionKind.KEEP_REMOTE
    assert out.primary.cursor() == remote.cursor()
    assert out.secondary is None


def test_reconcile_keep_both():
    local = TimelineSnapshot.build([_entry(i) for i in range(7)])
    remote = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])

    fork = TimelineFork.detect(local, remote)

    decision = TimelineReconcileDecision.from_fork_keep_both(fork)
    out = TimelineReconcile.apply(fork=fork, local=local, remote=remote, decision=decision)

    assert out.kind == ReconcileDecisionKind.KEEP_BOTH
    assert out.primary.cursor() == local.cursor()
    assert out.secondary is not None
    assert out.secondary.cursor() == remote.cursor()


def test_reconcile_rejects_mismatched_decision():
    local = TimelineSnapshot.build([_entry(i) for i in range(7)])
    remote = TimelineSnapshot.build([_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)])
    fork = TimelineFork.detect(local, remote)

    # forge wrong heads
    bad = TimelineReconcileDecision(
        kind=ReconcileDecisionKind.KEEP_LOCAL,
        local_head="a" * 64,
        remote_head="b" * 64,
        common_prefix_len=fork.common_prefix_len,
    )

    with pytest.raises(TimelineReconcileError):
        TimelineReconcile.apply(fork=fork, local=local, remote=remote, decision=bad)
