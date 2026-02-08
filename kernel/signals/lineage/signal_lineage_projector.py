# kernel/signals/lineage/signal_lineage_projector.py

from collections import defaultdict, deque, OrderedDict
from typing import Dict, Tuple

from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.signals.lineage.signal_lineage_view import SignalLineageView


def project_signal_lineage(
    view: SignalLineageView,
) -> Dict[int, Tuple[CanonicalSignalKey, ...]]:
    """
    Project a SignalLineageView into depth-indexed layers.

    Level 0 contains the root.
    Level N contains nodes at distance N from the root.

    This function is:
    - pure
    - deterministic
    - stable
    """

    # distance map: node -> minimal depth
    distances: Dict[CanonicalSignalKey, int] = {
        view.root: 0
    }

    queue = deque([view.root])

    while queue:
        current = queue.popleft()
        current_depth = distances[current]

        for parent in view.parent_map.get(current, ()):
            if parent not in distances:
                distances[parent] = current_depth + 1
                queue.append(parent)

    # group by depth
    layers: Dict[int, list[CanonicalSignalKey]] = defaultdict(list)

    for node, depth in distances.items():
        layers[depth].append(node)

    # deterministic ordering
    projection = OrderedDict()
    for depth in sorted(layers.keys()):
        projection[depth] = tuple(sorted(layers[depth], key=str))

    return projection