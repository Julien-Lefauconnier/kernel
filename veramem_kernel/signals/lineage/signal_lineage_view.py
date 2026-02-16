# kernel/signals/lineage/signal_lineage_view.py

from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple, Mapping

from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode


@dataclass(frozen=True)
class SignalLineageView:
    """
    Immutable projection of a SignalLineageNode.

    This view represents the resolved lineage graph for a signal:
    - parents
    - supersedes
    - full ancestor set
    - maximum depth

    It contains NO logic:
    - no validation
    - no timeline access
    - no inference
    """

    signal_key: CanonicalSignalKey
    parents: Tuple[CanonicalSignalKey, ...]
    supersedes: CanonicalSignalKey | None
    ancestors: FrozenSet[CanonicalSignalKey]
    depth: int

    # full adjacency (needed for projection)
    parent_map: Mapping[CanonicalSignalKey, Tuple[CanonicalSignalKey, ...]]
    # full node mapping (needed for patch applier & tests)
    node_map: Mapping[CanonicalSignalKey, SignalLineageNode]

    def __init__(
        self,
        signal_key: CanonicalSignalKey | None = None,
        parents: Tuple[CanonicalSignalKey, ...] = (),
        supersedes: CanonicalSignalKey | None = None,
        ancestors: FrozenSet[CanonicalSignalKey] = frozenset(),
        depth: int = 0,
        parent_map: Mapping[CanonicalSignalKey, Tuple[CanonicalSignalKey, ...]] | None = None,
        node_map: Mapping[CanonicalSignalKey, SignalLineageNode] | None = None,
        *,
        root: CanonicalSignalKey | None = None,
        nodes: Mapping[CanonicalSignalKey, SignalLineageNode] | None = None,
    ):
        if root is not None and nodes is not None:
            if not nodes:
                object.__setattr__(self, "signal_key", root)
                object.__setattr__(self, "parents", ())
                object.__setattr__(self, "supersedes", None)
                object.__setattr__(self, "ancestors", frozenset())
                object.__setattr__(self, "depth", 0)
                object.__setattr__(self, "parent_map", {})
                object.__setattr__(self, "_node_map", {})
                return

            root_node = nodes.get(root)
            if root_node is None:
                raise ValueError("Root node not found in nodes")


            rebuilt = build_signal_lineage_view(
                node=root_node,
                known_nodes=dict(nodes),
            )

            object.__setattr__(self, "signal_key", rebuilt.signal_key)
            object.__setattr__(self, "parents", rebuilt.parents)
            object.__setattr__(self, "supersedes", rebuilt.supersedes)
            object.__setattr__(self, "ancestors", rebuilt.ancestors)
            object.__setattr__(self, "depth", rebuilt.depth)
            object.__setattr__(self, "_node_map", dict(nodes))
            object.__setattr__(self, "parent_map", rebuilt.parent_map)
            return

        if signal_key is None or parent_map is None or node_map is None:
            raise TypeError("SignalLineageView requires canonical arguments")

        object.__setattr__(self, "signal_key", signal_key)
        object.__setattr__(self, "parents", parents)
        object.__setattr__(self, "supersedes", supersedes)
        object.__setattr__(self, "ancestors", ancestors)
        object.__setattr__(self, "depth", depth)
        object.__setattr__(self, "_node_map", node_map)
        object.__setattr__(self, "parent_map", parent_map)

    @property
    def root(self) -> CanonicalSignalKey:
        """
        Public semantic alias for the root signal of this lineage view.

        Exposed for resolver and projection consumers.
        """
        return self.signal_key
    
    @property
    def nodes(self) -> Mapping[CanonicalSignalKey, SignalLineageNode]:
        """
        All nodes involved in this lineage view.
        Public contract used by patch applier & tests.
        """
        return self.node_map

    @property
    def node_map(self) -> Mapping[CanonicalSignalKey, SignalLineageNode]:
        """
        Internal structural mapping.
        Used by patch applier and projections.
        """
        return self._node_map
    
    @property
    def node_keys(self) -> FrozenSet[CanonicalSignalKey]:
        """
        Set of all signal keys in this lineage view.
        Backward-compatible alias for diff / resolver.
        """
        return frozenset(self._node_map.keys())
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SignalLineageView):
            return False
        return (
            self.signal_key == other.signal_key
            and self.parents == other.parents
            and self.supersedes == other.supersedes
            and self.ancestors == other.ancestors
            and self.depth == other.depth
            and self.parent_map == other.parent_map
        )



def build_signal_lineage_view(
    node: SignalLineageNode,
    known_nodes: Dict[CanonicalSignalKey, SignalLineageNode],
) -> SignalLineageView:
    """
    Build a deterministic, immutable lineage view for a signal.

    Preconditions:
    - All lineage invariants have already been enforced.
    - `known_nodes` contains only valid, previously accepted nodes.

    This function is PURE and SIDE-EFFECT FREE.
    """

    visited: set[CanonicalSignalKey] = set()

    def walk(current_key: CanonicalSignalKey, current_depth: int):
        if current_key in visited:
            return set(), current_depth

        visited.add(current_key)

        node = known_nodes.get(current_key)
        if node is None:
            return set(), current_depth

        ancestors = set()
        max_depth = current_depth

        next_keys = list(node.parents)
        if node.supersedes is not None:
            next_keys.append(node.supersedes)

        for parent_key in next_keys:
            ancestors.add(parent_key)
            sub_ancestors, sub_depth = walk(parent_key, current_depth + 1)
            ancestors.update(sub_ancestors)
            max_depth = max(max_depth, sub_depth)

        return ancestors, max_depth

    # Start from this node's direct lineage
    root_keys = list(node.parents)
    if node.supersedes is not None:
        root_keys.append(node.supersedes)

    all_ancestors: set[CanonicalSignalKey] = set()
    depth = 0

    for key in root_keys:
        all_ancestors.add(key)
        sub_ancestors, sub_depth = walk(key, 1)
        all_ancestors.update(sub_ancestors)
        depth = max(depth, sub_depth)

    # Build full parent adjacency map for all nodes in the lineage
    parent_map: Dict[CanonicalSignalKey, Tuple[CanonicalSignalKey, ...]] = {}
    node_map: Dict[CanonicalSignalKey, SignalLineageNode] = {}

    for key in all_ancestors | {node.signal_key}:
        lineage_node = known_nodes.get(key)
        if lineage_node is None:
            continue

        parents = list(lineage_node.parents)
        if lineage_node.supersedes is not None:
            parents.append(lineage_node.supersedes)

        parent_map[key] = tuple(parents)
        node_map[key] = lineage_node

    return SignalLineageView(
        signal_key=node.signal_key,
        parents=node.parents,
        supersedes=node.supersedes,
        ancestors=frozenset(all_ancestors),
        depth=depth,
        parent_map=parent_map,
        node_map=node_map,
    )

    
