# kernel/signals/lineage/signal_lineage_resolver.py

from __future__ import annotations
from typing import Dict, Set


from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from veramem_kernel.signals.lineage.signal_lineage_view import SignalLineageView
from veramem_kernel.signals.lineage.signal_lineage_errors import (
    SignalLineageResolutionError,
)
from veramem_kernel.signals.lineage.signal_lineage_view import (
    build_signal_lineage_view,
)



def resolve_signal_lineage_view(
    root: CanonicalSignalKey,
    known_nodes: Dict[CanonicalSignalKey, SignalLineageNode],
) -> SignalLineageView:
    """
    Resolve a SignalLineageView starting from a root signal.

    This resolver is:
    - pure (no side effects)
    - structural only (no invariant checks)
    - deterministic

    It fails fast if the lineage graph is incomplete or inconsistent.
    """

    if root not in known_nodes:
        raise SignalLineageResolutionError(
            f"signal not found in known_nodes: {root}"
        )

    visited: Set[CanonicalSignalKey] = set()
    stack: Set[CanonicalSignalKey] = set()

    def walk(current: CanonicalSignalKey) -> None:
        if current in stack:
            raise SignalLineageResolutionError(
                f"cycle detected while resolving lineage at: {current}"
            )
        if current in visited:
            return
        
        stack.add(current)

        node = known_nodes.get(current)
        if node is None:
            raise SignalLineageResolutionError(
                f"missing lineage node for signal: {current}"
            )

        visited.add(current)

        for parent in node.parents:
            walk(parent)

        if node.supersedes is not None:
            walk(node.supersedes)

        stack.remove(current)

    walk(root)

    node = known_nodes[root]

    rebuilt = build_signal_lineage_view(node, known_nodes)

    return SignalLineageView(
        signal_key=rebuilt.signal_key,
        parents=rebuilt.parents,
        supersedes=rebuilt.supersedes,
        ancestors=rebuilt.ancestors,
        depth=rebuilt.depth,
        parent_map=rebuilt.parent_map,
        node_map=known_nodes,  
    )
