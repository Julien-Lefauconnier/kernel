# tests/test_signal_lineage_view_kernel.py

import pytest
from datetime import datetime, timezone, timezone

from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode

from veramem_kernel.signals.lineage.signal_lineage_view import (
    build_signal_lineage_view,
    SignalLineageView,
)

from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


def _cursor():
    return TimelineCursor(datetime.now(timezone.utc))


def test_signal_lineage_view_for_root_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    node_A = SignalLineageNode(
        signal_key=A,
        emitted_at=_cursor(),
        parents=(),
        supersedes=None,
    )

    view = build_signal_lineage_view(node_A, known_nodes={})

    assert isinstance(view, SignalLineageView)
    assert view.signal_key == A
    assert view.parents == ()
    assert view.supersedes is None
    assert view.depth == 0
    assert view.ancestors == frozenset()


def test_signal_lineage_view_simple_chain():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    node_A = SignalLineageNode(A, _cursor(), (), None)
    node_B = SignalLineageNode(B, _cursor(), (A,), None)
    node_C = SignalLineageNode(C, _cursor(), (B,), None)

    known_nodes = {
        A: node_A,
        B: node_B,
    }

    view = build_signal_lineage_view(node_C, known_nodes)

    assert view.signal_key == C
    assert view.parents == (B,)
    assert view.depth == 2
    assert view.ancestors == frozenset({A, B})


def test_signal_lineage_view_with_multiple_parents():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    node_A = SignalLineageNode(A, _cursor(), (), None)
    node_B = SignalLineageNode(B, _cursor(), (), None)
    node_C = SignalLineageNode(C, _cursor(), (A, B), None)

    known_nodes = {
        A: node_A,
        B: node_B,
    }

    view = build_signal_lineage_view(node_C, known_nodes)

    assert view.depth == 1
    assert view.ancestors == frozenset({A, B})


def test_signal_lineage_view_includes_supersedes_as_ancestor():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    node_A = SignalLineageNode(A, _cursor(), (), None)
    node_B = SignalLineageNode(B, _cursor(), (), A)

    known_nodes = {
        A: node_A,
    }

    view = build_signal_lineage_view(node_B, known_nodes)

    assert view.supersedes == A
    assert view.depth == 1
    assert view.ancestors == frozenset({A})


def test_signal_lineage_view_is_deterministic():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    node_A = SignalLineageNode(A, _cursor(), (), None)
    node_B = SignalLineageNode(B, _cursor(), (A,), None)

    known_nodes = {A: node_A}

    view1 = build_signal_lineage_view(node_B, known_nodes)
    view2 = build_signal_lineage_view(node_B, known_nodes)

    assert view1 == view2


def test_signal_lineage_view_is_immutable():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    node_A = SignalLineageNode(A, _cursor(), (), None)

    view = build_signal_lineage_view(node_A, {})

    with pytest.raises(Exception):
        view.depth = 42  # frozen dataclass expected
