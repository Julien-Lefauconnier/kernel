# tests/test_signal_lineage_patch_applier_kernel.py

import pytest

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


def _key(code: str) -> CanonicalSignalKey:
    return CanonicalSignalKey(
        CanonicalSignalCategory.OBSERVATION_STATE,
        code,
    )


def _cursor() -> TimelineCursor:
    return TimelineCursor.now()


def _node(key, parents=()):
    return SignalLineageNode(
        key=key,
        emitted_at=_cursor(),
        parents=parents,
        supersedes=None,
    )


# ---------------------------------------------------------------------------
# Core behavior
# ---------------------------------------------------------------------------

def test_patch_applier_returns_identical_view_when_no_patches():
    A = _key("A")

    view = SignalLineageView(
        root=A,
        nodes={A: _node(A)},
    )

    new_view = apply_signal_lineage_patches(view, ())

    assert new_view == view
    assert new_view is not view  # immutability


def test_patch_applier_applies_add_patch():
    A = _key("A")

    empty = SignalLineageView(root=A, nodes={})

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.ADD,
            signal=A,
        ),
    )

    new_view = apply_signal_lineage_patches(empty, patches)

    assert A in new_view.nodes
    assert new_view.root == A


def test_patch_applier_applies_remove_patch():
    A = _key("A")

    view = SignalLineageView(
        root=A,
        nodes={A: _node(A)},
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.REMOVE,
            signal=A,
        ),
    )

    new_view = apply_signal_lineage_patches(view, patches)

    assert new_view.nodes == {}


def test_patch_applier_applies_move_patch_changes_depth():
    A = _key("A")
    B = _key("B")

    view = SignalLineageView(
        root=B,
        nodes={
            A: _node(A),
            B: _node(B, parents=(A,)),
        },
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.MOVE,
            signal=B,
        ),
    )

    new_view = apply_signal_lineage_patches(view, patches)

    assert new_view.nodes[B].parents == ()
    assert new_view.nodes[A].parents == ()


def test_patch_applier_applies_rewire_parents_patch():
    A = _key("A")
    B = _key("B")
    C = _key("C")

    view = SignalLineageView(
        root=C,
        nodes={
            A: _node(A),
            B: _node(B),
            C: _node(C, parents=(A,)),
        },
    )

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.REWIRE_PARENTS,
            signal=C,
            parents=(B,),
        ),
    )

    new_view = apply_signal_lineage_patches(view, patches)

    assert new_view.nodes[C].parents == (B,)


# ---------------------------------------------------------------------------
# Ordering & determinism
# ---------------------------------------------------------------------------

def test_patch_applier_respects_patch_order():
    A = _key("A")
    B = _key("B")

    view = SignalLineageView(
        root=B,
        nodes={
            A: _node(A),
            B: _node(B, parents=(A,)),
        },
    )

    patches = (
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

    new_view = apply_signal_lineage_patches(view, patches)

    assert A not in new_view.nodes
    assert new_view.nodes[B].parents == ()


def test_patch_applier_is_deterministic():
    A = _key("A")

    view = SignalLineageView(root=A, nodes={})

    patches = (
        SignalLineagePatch(
            type=SignalLineagePatchType.ADD,
            signal=A,
        ),
    )

    v1 = apply_signal_lineage_patches(view, patches)
    v2 = apply_signal_lineage_patches(view, patches)

    assert v1 == v2
