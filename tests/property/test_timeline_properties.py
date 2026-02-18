# tests/property/test_timeline_properties.py

from hypothesis import given, strategies as st, settings
from datetime import datetime, timezone, timedelta

from veramem_kernel.journals.timeline.timeline_entry import (
    TimelineEntry,
    TimelineEntryNature,
)
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_merge import (
    TimelineMerge,
    TimelineMergeKind,
)


# ============================================================
# Strategies
# ============================================================

ASCII_SAFE = st.characters(min_codepoint=33, max_codepoint=126)

def utc_datetimes():
    """
    Hypothesis-safe UTC datetime generator.
    """
    return st.datetimes(
        min_value=datetime(1970, 1, 1),  # MUST be naive
        max_value=datetime(2100, 1, 1),
    ).map(lambda dt: dt.replace(tzinfo=timezone.utc))

@st.composite
def timeline_entries(draw, min_size=1, max_size=30):
    """
    Generate VALID timeline entries:
    - unique entry_id
    - monotonic timestamps
    - deterministic ordering
    """

    n = draw(st.integers(min_value=min_size, max_value=max_size))

    ids = draw(
        st.lists(
            st.text(alphabet=ASCII_SAFE, min_size=8, max_size=32),
            min_size=n,
            max_size=n,
            unique=True,
        )
    )

    base_ts = draw(utc_datetimes())

    entries = []

    for i, eid in enumerate(ids):
        entries.append(
            TimelineEntry(
                entry_id=eid,
                created_at=base_ts + timedelta(seconds=i),
                type=TimelineEntryType.SYSTEM_NOTICE,
                title=f"title-{i}",
                description=None,
                action_id=None,
                place_id=None,
                origin_ref="kernel",
                nature=TimelineEntryNature.EVENT,
            )
        )

    return entries


# ============================================================
# Snapshot properties
# ============================================================


@given(timeline_entries())
@settings(max_examples=200)
def test_snapshot_determinism(entries):
    s1 = TimelineSnapshot.build(entries)
    s2 = TimelineSnapshot.build(entries)

    assert s1 == s2
    assert s1.head == s2.head


@given(timeline_entries(min_size=2))
def test_snapshot_order_changes_head(entries):
    s1 = TimelineSnapshot.build(entries)
    s2 = TimelineSnapshot.build(list(reversed(entries)))

    assert s1.head != s2.head


@given(timeline_entries())
def test_snapshot_append_changes_head(entries):
    snap = TimelineSnapshot.build(entries)

    extra = entries[-1]
    new = TimelineSnapshot.build(entries + [extra])

    assert new.head != snap.head


# ============================================================
# Delta properties
# ============================================================


@given(timeline_entries(min_size=5))
def test_delta_roundtrip(entries):
    base = TimelineSnapshot.build(entries[:3])
    target = TimelineSnapshot.build(entries)

    delta = TimelineDelta.from_snapshots(base, target)
    out = delta.apply_to(base)

    assert out == target


@given(timeline_entries(min_size=5))
def test_delta_idempotence(entries):
    base = TimelineSnapshot.build(entries[:3])
    target = TimelineSnapshot.build(entries)

    delta = TimelineDelta.from_snapshots(base, target)

    out1 = delta.apply_to(base)
    out2 = delta.apply_to(base)

    assert out1 == out2


@given(timeline_entries(min_size=5))
def test_delta_target_consistency(entries):
    base = TimelineSnapshot.build(entries[:3])
    target = TimelineSnapshot.build(entries)

    delta = TimelineDelta.from_snapshots(base, target)
    out = delta.apply_to(base)

    assert out.head == target.head


# ============================================================
# Fork properties
# ============================================================


@given(
    timeline_entries(min_size=3),
    timeline_entries(min_size=3),
)
def test_fork_symmetry(prefix, suffix):
    base = TimelineSnapshot.build(prefix)

    a = TimelineSnapshot.build(prefix + suffix)
    b = TimelineSnapshot.build(prefix + list(reversed(suffix)))

    f1 = TimelineFork.detect(a, b)
    f2 = TimelineFork.detect(b, a)

    assert f1.common_prefix_len == f2.common_prefix_len


@given(timeline_entries(min_size=5))
def test_fork_identical(entries):
    s1 = TimelineSnapshot.build(entries)
    s2 = TimelineSnapshot.build(entries)

    fork = TimelineFork.detect(s1, s2)

    assert not fork.is_fork()
    assert fork.common_prefix_len == len(entries)


# ============================================================
# Merge properties
# ============================================================


@given(
    timeline_entries(min_size=3),
    timeline_entries(min_size=3),
)
def test_merge_convergence(prefix, suffix):
    base = TimelineSnapshot.build(prefix)

    a = TimelineSnapshot.build(prefix + suffix)
    b = TimelineSnapshot.build(prefix + list(reversed(suffix)))

    fork = TimelineFork.detect(a, b)

    res1 = TimelineMerge.try_merge(fork=fork, local=a, remote=b)
    res2 = TimelineMerge.try_merge(fork=fork, local=b, remote=a)

    if res1.kind == res2.kind == TimelineMergeKind.MERGED:
        assert res1.merged.head == res2.merged.head


@given(
    timeline_entries(min_size=3),
    timeline_entries(min_size=3),
    timeline_entries(min_size=3),
)
def test_merge_associativity(prefix, a_suf, b_suf):
    base = TimelineSnapshot.build(prefix)

    a = TimelineSnapshot.build(prefix + a_suf)
    b = TimelineSnapshot.build(prefix + b_suf)

    f = TimelineFork.detect(a, b)
    ab = TimelineMerge.try_merge(fork=f, local=a, remote=b)

    if ab.kind != TimelineMergeKind.MERGED:
        return

    c = TimelineSnapshot.build(prefix + a_suf + b_suf)

    f2 = TimelineFork.detect(ab.merged, c)
    abc = TimelineMerge.try_merge(fork=f2, local=ab.merged, remote=c)

    if abc.kind == TimelineMergeKind.MERGED:
        assert abc.merged is not None


# ============================================================
# Distributed invariants
# ============================================================


@given(timeline_entries(min_size=5))
def test_merge_is_deterministic(entries):
    base = TimelineSnapshot.build(entries[:3])
    a = TimelineSnapshot.build(entries[:3] + entries[3:])
    b = TimelineSnapshot.build(entries[:3] + list(reversed(entries[3:])))

    fork = TimelineFork.detect(a, b)

    r1 = TimelineMerge.try_merge(fork=fork, local=a, remote=b)
    r2 = TimelineMerge.try_merge(fork=fork, local=a, remote=b)

    assert r1 == r2


@given(timeline_entries(min_size=5))
def test_delta_replay_stability(entries):
    base = TimelineSnapshot.build(entries[:3])
    target = TimelineSnapshot.build(entries)

    delta = TimelineDelta.from_snapshots(base, target)

    # replay twice
    out1 = delta.apply_to(base)
    out2 = delta.apply_to(base)

    assert out1 == out2
