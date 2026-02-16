# kernel/signals/lineage/signal_lineage_diff.py

from dataclasses import dataclass
from typing import FrozenSet

from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.lineage.signal_lineage_view import SignalLineageView


@dataclass(frozen=True)
class SignalLineageDiff:
    """
    Immutable structural diff between two SignalLineageView instances.

    This diff is:
    - pure
    - deterministic
    - structural only

    It performs NO validation and NO inference.
    """

    added: FrozenSet[CanonicalSignalKey]
    removed: FrozenSet[CanonicalSignalKey]
    moved: FrozenSet[CanonicalSignalKey]
    changed_parents: FrozenSet[CanonicalSignalKey]

    @property
    def is_empty(self) -> bool:
        return (
            not self.added
            and not self.removed
            and not self.moved
            and not self.changed_parents
        )


def diff_signal_lineage(
    before: SignalLineageView,
    after: SignalLineageView,
) -> SignalLineageDiff:
    before_nodes = before.node_keys
    after_nodes = after.node_keys

    added = after_nodes - before_nodes
    removed = before_nodes - after_nodes

    common = before_nodes & after_nodes

    moved = set()
    changed_parents = set()

    # SUBJECT move = depth of the lineage changes
    if before.depth != after.depth:
        moved.add(after.root)

    for key in common:
        before_parents = before.parent_map.get(key, ())
        after_parents = after.parent_map.get(key, ())

        if set(before_parents) != set(after_parents):
            changed_parents.add(key)

    return SignalLineageDiff(
        added=frozenset(added),
        removed=frozenset(removed),
        moved=frozenset(moved),
        changed_parents=frozenset(changed_parents),
    )



def _depth_of(
    key: CanonicalSignalKey,
    view: SignalLineageView,
) -> int:
    """
    Compute the depth of a node relative to the view root.

    Root depth = 0
    Depth = shortest path to root via parents
    """
    if key == view.root:
        return 0

    parents = view.parent_map.get(key)
    if not parents:
        # Orphan node (should not happen in valid views)
        return view.depth

    return 1 + min(_depth_of(parent, view) for parent in parents)


