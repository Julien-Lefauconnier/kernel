# tests/test_signal_lineage_resolver_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from veramem_kernel.signals.lineage.signal_lineage_errors import (
    SignalLineageResolutionError,
)
from veramem_kernel.signals.lineage.signal_lineage_view import SignalLineageView
from veramem_kernel.signals.lineage.signal_lineage_resolver import (
    resolve_signal_lineage_view,
)
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def cursor():
    return TimelineCursor(datetime.now(timezone.utc))


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_signal_lineage_resolver_resolves_simple_chain():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    node_A = SignalLineageNode(
        signal_key=A,
        emitted_at=cursor(),
        parents=(),
        supersedes=None,
    )

    node_B = SignalLineageNode(
        signal_key=B,
        emitted_at=cursor(),
        parents=(A,),
        supersedes=None,
    )

    known_nodes = {
        A: node_A,
        B: node_B,
    }

    view = resolve_signal_lineage_view(B, known_nodes)

    assert isinstance(view, SignalLineageView)
    assert view.root == B
    assert view.node_keys == {A, B}


def test_signal_lineage_resolver_rejects_unknown_signal():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    with pytest.raises(SignalLineageResolutionError):
        resolve_signal_lineage_view(A, known_nodes={})


def test_signal_lineage_resolver_resolves_deep_chain():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")
    D = CanonicalSignalKey(category, "D")

    node_A = SignalLineageNode(A, cursor(), (), None)
    node_B = SignalLineageNode(B, cursor(), (A,), None)
    node_C = SignalLineageNode(C, cursor(), (B,), None)
    node_D = SignalLineageNode(D, cursor(), (C,), None)

    known_nodes = {
        A: node_A,
        B: node_B,
        C: node_C,
        D: node_D,
    }

    view = resolve_signal_lineage_view(D, known_nodes)

    assert view.root == D
    assert view.node_keys == {A, B, C, D}


def test_signal_lineage_resolver_rejects_missing_parent_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    node_B = SignalLineageNode(
        signal_key=B,
        emitted_at=cursor(),
        parents=(A,),
        supersedes=None,
    )

    known_nodes = {
        B: node_B,
        # A manquant volontairement
    }

    with pytest.raises(SignalLineageResolutionError):
        resolve_signal_lineage_view(B, known_nodes)


def test_signal_lineage_resolver_has_no_side_effects():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    node_A = SignalLineageNode(A, cursor(), (), None)

    known_nodes = {A: node_A}
    snapshot = dict(known_nodes)

    resolve_signal_lineage_view(A, known_nodes)

    assert known_nodes == snapshot
