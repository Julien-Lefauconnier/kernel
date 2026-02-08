# tests/test_signal_lineage_invariants_kernel.py

import pytest
from datetime import datetime

from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from kernel.signals.canonical.canonical_signal_spec import CanonicalSignalSpec
from kernel.signals.canonical.canonical_signal_registry import CanonicalSignalRegistry
from kernel.journals.timeline.timeline_cursor import TimelineCursor
from kernel.journals.timeline.timeline_entry import TimelineEntry
from kernel.journals.timeline.timeline_types import TimelineEntryType

from kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from kernel.signals.lineage.signal_lineage_errors import (
    SignalLineageInvariantViolation,
)

from kernel.journals.timeline.timeline_journal import (
    get_timeline_journal,
    reset_timeline_journal,
)
from kernel.invariants.signal.signal_lineage_invariants import (
    assert_no_self_parent,
    assert_signal_registered,
    assert_parents_registered,
    assert_supersedes_registered,
    assert_supersedes_in_parents,
    assert_parents_emitted_before_child,
    assert_no_cycle,
    assert_supersedes_emitted_before_child,
    assert_signal_lineage_invariants,
    assert_supersedes_allowed_by_spec,
)


def test_signal_lineage_rejects_self_parent():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    key = CanonicalSignalKey(category, "self_signal")

    spec = CanonicalSignalSpec(
        key=key,
        states_allowed=frozenset({"observed"}),
        subject_kinds=frozenset({"entity"}),
        supersession_allowed=True,
        origin_allowed=frozenset({"system"}),
    )

    CanonicalSignalRegistry.register(spec)

    cursor = TimelineCursor(1)

    node = SignalLineageNode(
        signal_key=key,
        emitted_at=cursor,
        parents=(key,),
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_no_self_parent(node)


def test_signal_lineage_rejects_unregistered_signal_key():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    key = CanonicalSignalKey(category, "unregistered_signal")

    cursor = TimelineCursor(1)

    node = SignalLineageNode(
        signal_key=key,
        emitted_at=cursor,
        parents=(),
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_signal_registered(node)

def test_signal_lineage_rejects_unregistered_parent():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    parent = CanonicalSignalKey(category, "parent_signal")
    child = CanonicalSignalKey(category, "child_signal")

    # On enregistre UNIQUEMENT l’enfant
    child_spec = CanonicalSignalSpec(
        key=child,
        states_allowed=frozenset({"observed"}),
        subject_kinds=frozenset({"entity"}),
        supersession_allowed=True,
        origin_allowed=frozenset({"system"}),
    )
    CanonicalSignalRegistry.register(child_spec)

    cursor = TimelineCursor(2)

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=cursor,
        parents=(parent,),  # parent non enregistré
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_parents_registered(node)

def test_signal_lineage_rejects_unregistered_supersedes():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    # On enregistre uniquement l’enfant
    child_spec = CanonicalSignalSpec(
        key=child,
        states_allowed=frozenset({"observed"}),
        subject_kinds=frozenset({"entity"}),
        supersession_allowed=True,
        origin_allowed=frozenset({"system"}),
    )
    CanonicalSignalRegistry.register(child_spec)

    cursor = TimelineCursor(2)

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=cursor,
        parents=(),
        supersedes=superseded,  # non enregistré
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_supersedes_registered(node)


def test_signal_lineage_rejects_supersedes_not_in_parents():
    CanonicalSignalRegistry._clear_for_tests()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    parent = CanonicalSignalKey(category, "parent_signal")
    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    for key in (parent, superseded, child):
        spec = CanonicalSignalSpec(
            key=key,
            states_allowed=frozenset({"observed"}),
            subject_kinds=frozenset({"entity"}),
            supersession_allowed=True,
            origin_allowed=frozenset({"system"}),
        )
        CanonicalSignalRegistry.register(spec)

    cursor = TimelineCursor(3)

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=cursor,
        parents=(parent,),
        supersedes=superseded,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_supersedes_in_parents(node)


def test_signal_lineage_rejects_parent_emitted_after_child():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    parent = CanonicalSignalKey(category, "parent_signal")
    child = CanonicalSignalKey(category, "child_signal")

    for key in (parent, child):
        spec = CanonicalSignalSpec(
            key=key,
            states_allowed=frozenset({"observed"}),
            subject_kinds=frozenset({"entity"}),
            supersession_allowed=True,
            origin_allowed=frozenset({"system"}),
        )
        CanonicalSignalRegistry.register(spec)

    journal = get_timeline_journal()

    # ⚠️ Parent émis APRÈS l’enfant
    journal.append(
        TimelineEntry.unsafe(
            entry_id="signal-child",
            created_at=datetime.fromtimestamp(1),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(child),
        )
    )

    journal.append(
        TimelineEntry.unsafe(
            entry_id="signal-parent",
            created_at=datetime.fromtimestamp(2),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(parent),
        )
    )

    child_cursor = TimelineCursor(datetime.fromtimestamp(1))

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=child_cursor,
        parents=(parent,),
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_parents_emitted_before_child(node)


def test_signal_lineage_allows_simple_chain_without_cycle():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    nodes = {
        B: SignalLineageNode(
            signal_key=B,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(A,),
            supersedes=None,
        ),
        C: SignalLineageNode(
            signal_key=C,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(B,),
            supersedes=None,
        ),
    }

    node = SignalLineageNode(
        signal_key=A,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(),
        supersedes=None,
    )

    # ne doit PAS lever
    assert_no_cycle(node, nodes)


def test_signal_lineage_rejects_direct_indirect_cycle():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    nodes = {
        A: SignalLineageNode(
            signal_key=A,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(B,),
            supersedes=None,
        )
    }

    node = SignalLineageNode(
        signal_key=B,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(A,),
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_no_cycle(node, nodes)


def test_signal_lineage_rejects_long_cycle():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")

    nodes = {
        A: SignalLineageNode(
            signal_key=A,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(B,),
            supersedes=None,
        ),
        B: SignalLineageNode(
            signal_key=B,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(C,),
            supersedes=None,
        ),
    }

    node = SignalLineageNode(
        signal_key=C,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(A,),
        supersedes=None,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_no_cycle(node, nodes)


def test_signal_lineage_rejects_cycle_via_supersedes():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    nodes = {
        B: SignalLineageNode(
            signal_key=B,
            emitted_at=TimelineCursor(datetime.utcnow()),
            parents=(A,),
            supersedes=None,
        )
    }

    node = SignalLineageNode(
        signal_key=A,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(),
        supersedes=B,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_no_cycle(node, nodes)


def test_signal_lineage_rejects_supersedes_emitted_after_child():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    for key in (superseded, child):
        CanonicalSignalRegistry.register(
            CanonicalSignalSpec(
                key=key,
                states_allowed=frozenset({"observed"}),
                subject_kinds=frozenset({"entity"}),
                supersession_allowed=True,
                origin_allowed=frozenset({"system"}),
            )
        )

    journal = get_timeline_journal()

    # enfant émis en premier
    journal.append(
        TimelineEntry.unsafe(
            entry_id="child",
            created_at=datetime.fromtimestamp(1),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(child),
        )
    )

    # superseded émis APRÈS
    journal.append(
        TimelineEntry.unsafe(
            entry_id="superseded",
            created_at=datetime.fromtimestamp(2),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(superseded),
        )
    )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.fromtimestamp(1)),
        parents=(),
        supersedes=superseded,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_supersedes_emitted_before_child(node)


def test_signal_lineage_rejects_supersedes_never_emitted():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "ghost_signal")
    child = CanonicalSignalKey(category, "new_signal")

    for key in (superseded, child):
        CanonicalSignalRegistry.register(
            CanonicalSignalSpec(
                key=key,
                states_allowed=frozenset({"observed"}),
                subject_kinds=frozenset({"entity"}),
                supersession_allowed=True,
                origin_allowed=frozenset({"system"}),
            )
        )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.fromtimestamp(2)),
        parents=(),
        supersedes=superseded,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_supersedes_emitted_before_child(node)


def test_signal_lineage_allows_valid_supersedes_temporally():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    for key in (superseded, child):
        CanonicalSignalRegistry.register(
            CanonicalSignalSpec(
                key=key,
                states_allowed=frozenset({"observed"}),
                subject_kinds=frozenset({"entity"}),
                supersession_allowed=True,
                origin_allowed=frozenset({"system"}),
            )
        )

    journal = get_timeline_journal()

    journal.append(
        TimelineEntry.unsafe(
            entry_id="superseded",
            created_at=datetime.fromtimestamp(1),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(superseded),
        )
    )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.fromtimestamp(2)),
        parents=(),
        supersedes=superseded,
    )

    # ne doit PAS lever
    assert_supersedes_emitted_before_child(node)


def test_signal_lineage_composite_invariant_passes_on_valid_node():
    category = CanonicalSignalCategory.OBSERVATION_STATE

    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    for key in (A, B):
        CanonicalSignalRegistry.register(
            CanonicalSignalSpec(
                key=key,
                states_allowed=frozenset({"observed"}),
                subject_kinds=frozenset({"entity"}),
                supersession_allowed=True,
                origin_allowed=frozenset({"system"}),
            )
        )

    reset_timeline_journal()
    journal = get_timeline_journal()

    journal.append(
        TimelineEntry.unsafe(
            entry_id="A",
            created_at=datetime.fromtimestamp(1),
            type=TimelineEntryType.SYSTEM_NOTICE,
            title="Signal emitted",
            description=None,
            action_id=None,
            origin_ref=str(A),
        )
    )

    node_A = SignalLineageNode(
        signal_key=A,
        emitted_at=TimelineCursor(datetime.fromtimestamp(1)),
        parents=(),
        supersedes=None,
    )

    node_B = SignalLineageNode(
        signal_key=B,
        emitted_at=TimelineCursor(datetime.fromtimestamp(2)),
        parents=(A,),
        supersedes=None,
    )

    known_nodes = {A: node_A}

    # ne doit PAS lever
    assert_signal_lineage_invariants(node_B, known_nodes)


def test_signal_lineage_rejects_supersedes_when_not_allowed_by_spec():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    # superseded peut être supersédé, child NON
    CanonicalSignalRegistry.register(
        CanonicalSignalSpec(
            key=superseded,
            states_allowed=frozenset({"observed"}),
            subject_kinds=frozenset({"entity"}),
            supersession_allowed=True,
            origin_allowed=frozenset({"system"}),
        )
    )

    CanonicalSignalRegistry.register(
        CanonicalSignalSpec(
            key=child,
            states_allowed=frozenset({"observed"}),
            subject_kinds=frozenset({"entity"}),
            supersession_allowed=False,  # ⛔ interdit
            origin_allowed=frozenset({"system"}),
        )
    )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(),
        supersedes=superseded,
    )

    with pytest.raises(SignalLineageInvariantViolation):
        assert_supersedes_allowed_by_spec(node)


def test_signal_lineage_allows_supersedes_when_allowed_by_spec():
    CanonicalSignalRegistry._clear_for_tests()
    reset_timeline_journal()

    category = CanonicalSignalCategory.OBSERVATION_STATE

    superseded = CanonicalSignalKey(category, "old_signal")
    child = CanonicalSignalKey(category, "new_signal")

    for key in (superseded, child):
        CanonicalSignalRegistry.register(
            CanonicalSignalSpec(
                key=key,
                states_allowed=frozenset({"observed"}),
                subject_kinds=frozenset({"entity"}),
                supersession_allowed=True,  # ✅ autorisé
                origin_allowed=frozenset({"system"}),
            )
        )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(),
        supersedes=superseded,
    )

    # ne doit PAS lever
    assert_supersedes_allowed_by_spec(node)


def test_signal_lineage_ignores_spec_when_no_supersedes():
    CanonicalSignalRegistry._clear_for_tests()

    category = CanonicalSignalCategory.OBSERVATION_STATE
    child = CanonicalSignalKey(category, "new_signal")

    CanonicalSignalRegistry.register(
        CanonicalSignalSpec(
            key=child,
            states_allowed=frozenset({"observed"}),
            subject_kinds=frozenset({"entity"}),
            supersession_allowed=False,
            origin_allowed=frozenset({"system"}),
        )
    )

    node = SignalLineageNode(
        signal_key=child,
        emitted_at=TimelineCursor(datetime.utcnow()),
        parents=(),
        supersedes=None,
    )

    # ne doit PAS lever
    assert_supersedes_allowed_by_spec(node)


