# kernel/signals/lineage/signal_lineage_patch_applier.py

from typing import Iterable, Dict

from veramem_kernel.signals.lineage.signal_lineage_patch import (
    SignalLineagePatch,
    SignalLineagePatchType,
)
from veramem_kernel.signals.lineage.signal_lineage_node import SignalLineageNode
from veramem_kernel.signals.lineage.signal_lineage_view import (
    SignalLineageView,
    build_signal_lineage_view,
)
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


def apply_signal_lineage_patches(
    view: SignalLineageView,
    patches: Iterable[SignalLineagePatch],
) -> SignalLineageView:
    """
    Apply a sequence of SignalLineagePatch to a SignalLineageView.

    This function is PURE and DETERMINISTIC.
    """

    # Rebuild mutable working set of nodes
    nodes: Dict = {}

    # Recreate nodes from the existing view
    for key, parents in view.parent_map.items():
        nodes[key] = SignalLineageNode(
            signal_key=key,
            emitted_at=TimelineCursor.now(),
            parents=parents,
            supersedes=None,
        )

    # Apply patches in order
    for patch in patches:
        key = patch.key

        if patch.type is SignalLineagePatchType.ADD:
            nodes[key] = SignalLineageNode(
                signal_key=key,
                emitted_at=TimelineCursor.now(),
                parents=patch.parents or (),
                supersedes=None,
            )

        elif patch.type is SignalLineagePatchType.REMOVE:
            nodes.pop(key, None)

            # Also remove it from parents elsewhere
            for k, node in list(nodes.items()):
                if key in node.parents:
                    nodes[k] = SignalLineageNode(
                        signal_key=k,
                        emitted_at=node.emitted_at,
                        parents=tuple(p for p in node.parents if p != key),
                        supersedes=node.supersedes,
                    )

        elif patch.type is SignalLineagePatchType.MOVE:
            # MOVE = structural change without parent mutation
            # Depth change is implicit via reprojection
            node = nodes.get(key)
            if node is None:
                continue

            # Preserve old parents as independent roots
            old_parents = node.parents

            # Detach moved node
            nodes[key] = SignalLineageNode(
                signal_key=key,
                emitted_at=node.emitted_at,
                parents=(),
                supersedes=node.supersedes,
            )

            # Ensure former parents remain as root-level nodes
            for parent_key in old_parents:
                parent_node = nodes.get(parent_key)
                if parent_node is None:
                    continue
                if parent_node.parents:
                    nodes[parent_key] = SignalLineageNode(
                        signal_key=parent_key,
                        emitted_at=parent_node.emitted_at,
                        parents=(),
                        supersedes=parent_node.supersedes,
                    )

        elif patch.type is SignalLineagePatchType.REWIRE_PARENTS:
            node = nodes.get(key)
            if node is None:
                continue

            nodes[key] = SignalLineageNode(
                signal_key=key,
                emitted_at=node.emitted_at,
                parents=patch.parents or (),
                supersedes=node.supersedes,
            )

        else:
            raise ValueError(f"Unsupported patch type: {patch.type}")

    # Reproject final view from root
    root_node = nodes.get(view.root)
    if root_node is None:
        # Graph is now empty
        return SignalLineageView(
            root=view.root,
            nodes={},
        )

    rebuilt = build_signal_lineage_view(
        node=root_node,
        known_nodes=nodes,
    )

    return SignalLineageView(
        signal_key=rebuilt.signal_key,
        parents=rebuilt.parents,
        supersedes=rebuilt.supersedes,
        ancestors=rebuilt.ancestors,
        depth=rebuilt.depth,
        parent_map=rebuilt.parent_map,
        node_map=nodes,  
    )
