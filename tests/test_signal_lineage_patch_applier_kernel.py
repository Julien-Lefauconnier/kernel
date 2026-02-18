# tests/test_signal_lineage_patch_applier_kernel.py

from __future__ import annotations

import pytest
from datetime import datetime, timezone

from veramem_kernel.signals.lineage.signal_lineage_patch_applier import (
    apply_signal_lineage_patches,
)
from veramem_kernel.signals.lineage.signal_lineage_patch import (
    SignalLineagePatch,
    SignalLineagePatchType,
)
from veramem_kernel.signals.lineage.signal_lineage_view import SignalLineageView
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from veramem_kernel.signals.canonical.canonical_signal_key import (
    CanonicalSignalKey,
    CanonicalSignalCategory,
)
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


# -----------------------------------------------------------------------------
# Deterministic helpers (industrial kernel style: no wall-clock dependency)
# -----------------------------------------------------------------------------

_TEST_EPOCH = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def _ts(seconds: int) -> datetime:
    return _TEST_EPOCH.replace(second=_TEST_EPOCH.second + seconds)


def _cursor_at(seconds: int) -> TimelineCursor:
    return TimelineCursor(_ts(seconds))


def _emitted_at(seconds: int = 0) -> TimelineCursor:
    # Single deterministic anchor for patch application
    return _cursor_at(seconds)


def _key(code: str) -> CanonicalSignalKey:
    return CanonicalSignalKey(CanonicalSignalCategory.OBSERVATION_STATE, code)


def _node(key: CanonicalSignalKey, *, emitted_at: TimelineCursor, parents=()) -> SignalLineageNode:
    # NOTE: SignalLineageNode ctor uses field name `signal_key` (not `key`)
    return SignalLineageNode(
        signal_key=key,
        emitted_at=emitted_at,
        parents=tuple(parents),
        supersedes=None,
    )


# -----------------------------------------------------------------------------
# Core behavior
# -----------------------------------------------------------------------------

def test_patch_applier_returns_identical_view_when_no_patches():
    A = _key("A")

    view = SignalLineageView(
        root=A,
        nodes={A: _node(A, emitted_at=_cursor_at(1))},
    )

    new_view = apply_signal_lineage_patches(
        view,
        (),
        emitted_at=_emitted_at(10),
    )

    assert new_view == view
    assert new_view is not view  # immutability / functional update


def test_patch_applier_applies_add_patch():
    A = _key("A")

    empty = SignalLineageView(root=A, nodes={})

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.ADD,
            signal=A,
        ),
    )

    new_view = apply_signal_lineage_patches(
        empty,
        patches,
        emitted_at=_emitted_at(10),
    )

    assert new_view.root == A
    assert A in new_view.nodes


def test_patch_applier_applies_remove_patch():
    A = _key("A")

    view = SignalLineageView(
        root=A,
        nodes={A: _node(A, emitted_at=_cursor_at(1))},
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.REMOVE,
            signal=A,
        ),
    )

    new_view = apply_signal_lineage_patches(
        view,
        patches,
        emitted_at=_emitted_at(10),
    )

    assert new_view.nodes == {}


def test_patch_applier_applies_move_patch_changes_depth():
    A = _key("A")
    B = _key("B")

    view = SignalLineageView(
        root=B,
        nodes={
            A: _node(A, emitted_at=_cursor_at(1)),
            B: _node(B, emitted_at=_cursor_at(2), parents=(A,)),
        },
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.MOVE,
            signal=B,
        ),
    )

    new_view = apply_signal_lineage_patches(
        view,
        patches,
        emitted_at=_emitted_at(10),
    )

    assert new_view.nodes[B].parents == ()
    assert new_view.nodes[A].parents == ()


def test_patch_applier_applies_rewire_parents_patch():
    A = _key("A")
    B = _key("B")
    C = _key("C")

    # Build a view where B is guaranteed to exist in the working set.
    # Some implementations rebuild from parent_map only,
    # so we ensure B appears as a parent AND as a child.
    view = SignalLineageView(
        root=C,
        nodes={
            A: _node(A, emitted_at=_cursor_at(1)),
            B: _node(B, emitted_at=_cursor_at(2), parents=(A,)),
            C: _node(C, emitted_at=_cursor_at(3), parents=(B,)),  # <- key fix
        },
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.REWIRE_PARENTS,
            signal=C,
            parents=(B,),
        ),
    )

    new_view = apply_signal_lineage_patches(
        view,
        patches,
        emitted_at=_emitted_at(10),
    )

    assert new_view.nodes[C].parents == (B,)




# -----------------------------------------------------------------------------
# Ordering & determinism
# -----------------------------------------------------------------------------

def test_patch_applier_respects_patch_order():
    A = _key("A")
    B = _key("B")

    view = SignalLineageView(
        root=B,
        nodes={
            A: _node(A, emitted_at=_cursor_at(1)),
            B: _node(B, emitted_at=_cursor_at(2), parents=(A,)),
        },
    )

    patches = (
        # rewire first, then remove parent node
        SignalLineagePatch(
            type=SignalLineagePatchType.REWIRE_PARENTS,
            signal=B,
            parents=(),
        ),
        SignalLineagePatch(
            type=SignalLineagePatchType.REMOVE,
            signal=A,
        ),
    )

    new_view = apply_signal_lineage_patches(
        view,
        patches,
        emitted_at=_emitted_at(10),
    )

    assert A not in new_view.nodes
    assert new_view.nodes[B].parents == ()


def test_patch_applier_is_deterministic_for_same_inputs_and_anchor():
    A = _key("A")

    view = SignalLineageView(root=A, nodes={})

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.ADD,
            signal=A,
        ),
    )

    anchor = _emitted_at(10)

    v1 = apply_signal_lineage_patches(view, patches, emitted_at=anchor)
    v2 = apply_signal_lineage_patches(view, patches, emitted_at=anchor)

    assert v1 == v2
    assert v1 is not v2  # functional update, no mutation
