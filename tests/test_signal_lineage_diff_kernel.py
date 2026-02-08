# tests/test_signal_lineage_diff_kernel.py

from kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from kernel.signals.lineage.signal_lineage_view import build_signal_lineage_view
from kernel.signals.lineage.signal_lineage_diff import diff_signal_lineage
from kernel.journals.timeline.timeline_cursor import TimelineCursor


def _cursor():
    # Helper local de test, explicite et déterministe dans l’intention
    return TimelineCursor.now()


def _build_view(root, nodes):
    return build_signal_lineage_view(nodes[root], nodes)


def test_signal_lineage_diff_is_empty_for_identical_views():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    nodes = {A: SignalLineageNode(A, _cursor(), (), None)}
    view = _build_view(A, nodes)

    diff = diff_signal_lineage(view, view)

    assert diff.is_empty
    assert diff.added == frozenset()
    assert diff.removed == frozenset()
    assert diff.moved == frozenset()
    assert diff.changed_parents == frozenset()


def test_signal_lineage_diff_detects_added_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    before_nodes = {A: SignalLineageNode(A, _cursor(), (), None)}
    after_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (A,), None),
    }

    before = _build_view(A, before_nodes)
    after = _build_view(B, after_nodes)

    diff = diff_signal_lineage(before, after)

    assert diff.added == frozenset({B})
    assert diff.removed == frozenset()
    assert not diff.is_empty


def test_signal_lineage_diff_detects_removed_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    before_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (A,), None),
    }
    after_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
    }

    before = _build_view(B, before_nodes)
    after = _build_view(A, after_nodes)

    diff = diff_signal_lineage(before, after)

    assert diff.removed == frozenset({B})
    assert diff.added == frozenset()
    assert not diff.is_empty


def test_signal_lineage_diff_detects_depth_change():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    before_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (A,), None),
        C: SignalLineageNode(C, _cursor(), (B,), None),
    }

    after_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (A,), None),
        C: SignalLineageNode(C, _cursor(), (A,), None),  # depth change
    }

    before = _build_view(C, before_nodes)
    after = _build_view(C, after_nodes)

    diff = diff_signal_lineage(before, after)

    assert diff.moved == frozenset({C})
    assert not diff.is_empty


def test_signal_lineage_diff_detects_parent_change():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    before_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (), None),
        C: SignalLineageNode(C, _cursor(), (A,), None),
    }

    after_nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (), None),
        C: SignalLineageNode(C, _cursor(), (B,), None),
    }

    before = _build_view(C, before_nodes)
    after = _build_view(C, after_nodes)

    diff = diff_signal_lineage(before, after)

    assert diff.changed_parents == frozenset({C})
    assert not diff.is_empty


def test_signal_lineage_diff_is_deterministic():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    nodes = {
        A: SignalLineageNode(A, _cursor(), (), None),
        B: SignalLineageNode(B, _cursor(), (A,), None),
    }

    view1 = _build_view(B, nodes)
    view2 = _build_view(B, nodes)

    d1 = diff_signal_lineage(view1, view2)
    d2 = diff_signal_lineage(view1, view2)

    assert d1 == d2
