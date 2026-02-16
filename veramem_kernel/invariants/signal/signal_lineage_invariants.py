# kernel/invariants/signal/signal_lineage_invariants.py

from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from veramem_kernel.signals.lineage.signal_lineage_errors import (
    SignalLineageInvariantViolation,
)
from veramem_kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
)
from veramem_kernel.journals.timeline.timeline_journal import get_timeline_journal


def assert_no_self_parent(node: SignalLineageNode) -> None:
    if node.signal_key in node.parents:
        raise SignalLineageInvariantViolation(
            "signal cannot list itself as a parent"
        )

def assert_signal_registered(node: SignalLineageNode) -> None:
    if not CanonicalSignalRegistry.has(node.signal_key):
        raise SignalLineageInvariantViolation(
            f"signal not registered: {node.signal_key}"
        )

def assert_parents_registered(node: SignalLineageNode) -> None:
    for parent in node.parents:
        if not CanonicalSignalRegistry.has(parent):
            raise SignalLineageInvariantViolation(
                f"parent signal not registered: {parent}"
            )

def assert_supersedes_registered(node: SignalLineageNode) -> None:
    if node.supersedes is None:
        return
    if not CanonicalSignalRegistry.has(node.supersedes):
        raise SignalLineageInvariantViolation(
            f"superseded signal not registered: {node.supersedes}"
        )

def assert_supersedes_in_parents(node: SignalLineageNode) -> None:
    if node.supersedes is None:
        return
    if node.supersedes not in node.parents:
        raise SignalLineageInvariantViolation(
            "superseded signal must be included in parents"
        )

def assert_parents_emitted_before_child(node: SignalLineageNode) -> None:
    journal = get_timeline_journal()
    entries = journal.list_events()

    first_seen = {}

    for entry in entries:
        if entry.origin_ref is None:
            continue

        first_seen.setdefault(entry.origin_ref, entry.timestamp)

    for parent in node.parents:
        parent_ts = first_seen.get(str(parent))
        if parent_ts is None or parent_ts >= node.emitted_at.timestamp:
            raise SignalLineageInvariantViolation(
                "parent must be emitted before child"
            )

def assert_no_cycle(
    node: SignalLineageNode,
    known_nodes: dict,
) -> None:
    """
    Reject any direct or indirect cycle in signal lineage.

    The check is purely local:
    - `node` is the lineage node being validated
    - `known_nodes` contains already-known lineage nodes
      (keyed by CanonicalSignalKey)

    supersedes is treated as a parent for cycle detection.
    """

    target = node.signal_key
    visited = set()

    def walk(current_key):
        # If we come back to the target, we found a cycle
        if current_key == target:
            raise SignalLineageInvariantViolation(
                "signal lineage cycle detected"
            )

        if current_key in visited:
            return

        visited.add(current_key)

        parent_node = known_nodes.get(current_key)
        if parent_node is None:
            return

        # Collect parents + supersedes (if any)
        next_parents = list(parent_node.parents)
        if parent_node.supersedes is not None:
            next_parents.append(parent_node.supersedes)

        for p in next_parents:
            walk(p)

    # Start from all parents of the node being validated
    initial_parents = list(node.parents)
    if node.supersedes is not None:
        initial_parents.append(node.supersedes)

    for parent in initial_parents:
        walk(parent)

def assert_supersedes_emitted_before_child(node: SignalLineageNode) -> None:
    """
    Ensure that a superseded signal was emitted strictly before the current signal.

    This invariant is temporal and factual:
    - it reads the timeline
    - it relies on origin_ref to identify emitted signals
    """

    if node.supersedes is None:
        return

    journal = get_timeline_journal()
    entries = journal.list_events()

    superseded_key = str(node.supersedes)
    first_seen_ts = None

    for entry in entries:
        if entry.origin_ref != superseded_key:
            continue

        first_seen_ts = entry.timestamp
        break

    if first_seen_ts is None:
        raise SignalLineageInvariantViolation(
            "superseded signal was never emitted"
        )

    if first_seen_ts >= node.emitted_at.timestamp:
        raise SignalLineageInvariantViolation(
            "superseded signal must be emitted before the superseding signal"
        )


def assert_signal_lineage_invariants(
    node: SignalLineageNode,
    known_nodes: dict,
) -> None:
    """
    Enforce the full Signal Lineage invariant contract.

    This function is the ONLY public entrypoint for lineage validation.
    """

    # --- Structural ---
    assert_no_self_parent(node)
    assert_signal_registered(node)
    assert_parents_registered(node)
    assert_supersedes_registered(node)
    assert_supersedes_in_parents(node)

    # --- Temporal ---
    assert_parents_emitted_before_child(node)
    assert_supersedes_emitted_before_child(node)

    # --- Graph consistency ---
    assert_no_cycle(node, known_nodes)


def assert_supersedes_allowed_by_spec(node: SignalLineageNode) -> None:
    if node.supersedes is None:
        return

    spec = CanonicalSignalRegistry.get(node.signal_key)

    if not spec.supersession_allowed:
        raise SignalLineageInvariantViolation(
            "supersedes is not allowed by canonical signal spec"
        )
