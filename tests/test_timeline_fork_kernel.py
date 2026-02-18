# tests/test_timeline_fork_kernel.py

from datetime import datetime, timezone

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork, TimelineForkKind


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


def test_fork_identical():
    a = _snapshot(5)
    b = _snapshot(5)

    fork = TimelineFork.detect(a, b)
    fork.assert_consistent()

    assert fork.kind == TimelineForkKind.IDENTICAL
    assert fork.common_prefix_len == 5
    assert fork.left_suffix == ()
    assert fork.right_suffix == ()


def test_fork_extension_right_extends_left():
    base = _snapshot(5)
    extended = _snapshot(8)

    fork = TimelineFork.detect(base, extended)
    fork.assert_consistent()

    assert fork.kind == TimelineForkKind.EXTENDS_LEFT
    assert fork.common_prefix_len == 5
    assert fork.left_suffix == ()
    assert len(fork.right_suffix) == 3


def test_fork_extension_left_extends_right():
    extended = _snapshot(8)
    base = _snapshot(5)

    fork = TimelineFork.detect(extended, base)
    fork.assert_consistent()

    assert fork.kind == TimelineForkKind.EXTENDS_RIGHT
    assert fork.common_prefix_len == 5
    assert len(fork.left_suffix) == 3
    assert fork.right_suffix == ()


def test_fork_detects_divergence_midway():
    # Common prefix: first 4 entries
    left = TimelineSnapshot.build([_entry(i) for i in range(7)])

    # Right diverges at index 4 by replacing entry-004 with entry-999,
    # then continues with new suffix entries.
    right_entries = [_entry(i) for i in range(4)] + [_entry(999), _entry(1000), _entry(1001)]
    right = TimelineSnapshot.build(right_entries)

    fork = TimelineFork.detect(left, right)
    fork.assert_consistent()

    assert fork.kind == TimelineForkKind.FORK
    assert fork.common_prefix_len == 4
    assert len(fork.left_suffix) == 3  # left has 7 total => 7-4
    assert len(fork.right_suffix) == 3 # right has 7 total => 7-4
    assert fork.is_fork() is True


def test_fork_disjoint_prefix_len_zero():
    left = TimelineSnapshot.build([_entry(1), _entry(2), _entry(3)])
    right = TimelineSnapshot.build([_entry(999), _entry(1000)])

    fork = TimelineFork.detect(left, right)
    fork.assert_consistent()

    assert fork.kind == TimelineForkKind.FORK
    assert fork.common_prefix_len == 0
    assert len(fork.left_suffix) == 3
    assert len(fork.right_suffix) == 2


def test_fork_is_deterministic():
    a = _snapshot(6)
    b = _snapshot(9)

    f1 = TimelineFork.detect(a, b)
    f2 = TimelineFork.detect(a, b)

    assert f1 == f2
