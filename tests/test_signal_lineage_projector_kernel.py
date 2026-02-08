# tests/test_signal_lineage_projector_kernel.py

import pytest
from datetime import datetime

from kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from kernel.signals.lineage.signal_lineage_view import build_signal_lineage_view
from kernel.signals.lineage.signal_lineage_projector import project_signal_lineage


def cursor():
    from kernel.journals.timeline.timeline_cursor import TimelineCursor
    return TimelineCursor(datetime.utcnow())


def test_signal_lineage_projector_projects_single_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    node = SignalLineageNode(A, cursor(), (), None)
    view = build_signal_lineage_view(node, {A: node})

    projection = project_signal_lineage(view)

    assert projection == {
        0: (A,)
    }


def test_signal_lineage_projector_projects_simple_chain():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    node_A = SignalLineageNode(A, cursor(), (), None)
    node_B = SignalLineageNode(B, cursor(), (A,), None)

    view = build_signal_lineage_view(
        node_B,
        {
            A: node_A,
            B: node_B,
        }
    )

    projection = project_signal_lineage(view)

    assert projection == {
        0: (B,),
        1: (A,),
    }


def test_signal_lineage_projector_projects_deep_chain():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")
    D = CanonicalSignalKey(category, "D")

    nodes = {
        A: SignalLineageNode(A, cursor(), (), None),
        B: SignalLineageNode(B, cursor(), (A,), None),
        C: SignalLineageNode(C, cursor(), (B,), None),
        D: SignalLineageNode(D, cursor(), (C,), None),
    }

    view = build_signal_lineage_view(nodes[D], nodes)
    projection = project_signal_lineage(view)

    assert projection == {
        0: (D,),
        1: (C,),
        2: (B,),
        3: (A,),
    }


def test_signal_lineage_projector_projects_branching_graph():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")
    D = CanonicalSignalKey(category, "D")

    nodes = {
        A: SignalLineageNode(A, cursor(), (), None),
        B: SignalLineageNode(B, cursor(), (A,), None),
        C: SignalLineageNode(C, cursor(), (A,), None),
        D: SignalLineageNode(D, cursor(), (B, C), None),
    }

    view = build_signal_lineage_view(nodes[D], nodes)
    projection = project_signal_lineage(view)

    assert projection[0] == (D,)
    assert set(projection[1]) == {B, C}
    assert projection[2] == (A,)


def test_signal_lineage_projector_is_deterministic():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    nodes = {
        A: SignalLineageNode(A, cursor(), (), None),
        B: SignalLineageNode(B, cursor(), (A,), None),
        C: SignalLineageNode(C, cursor(), (A,), None),
    }

    view = build_signal_lineage_view(nodes[C], nodes)

    p1 = project_signal_lineage(view)
    p2 = project_signal_lineage(view)

    assert p1 == p2
