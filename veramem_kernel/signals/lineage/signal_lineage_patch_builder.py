# veramem_kernel/signals/lineage/signal_lineage_patch_builder.py

from typing import Tuple

from veramem_kernel.signals.lineage.signal_lineage_view import SignalLineageView
from veramem_kernel.signals.lineage.signal_lineage_diff import SignalLineageDiff
from veramem_kernel.signals.lineage.signal_lineage_patch import (
    SignalLineagePatch,
    SignalLineagePatchType,
)


def build_signal_lineage_patches(
    diff: SignalLineageDiff,
) -> Tuple[SignalLineagePatch, ...]:
    """
    Build an ordered, deterministic sequence of SignalLineagePatch
    from a SignalLineageDiff.

    Ordering is canonical and stable:
    1. REMOVES
    2. ADDS
    3. MOVES
    4. REWIRE_PARENTS

    This function is PURE and SIDE-EFFECT FREE.
    """
    

    patches: list[SignalLineagePatch] = []

    # 1. Removals
    for key in sorted(diff.removed):
        patches.append(
            SignalLineagePatch(
                type=SignalLineagePatchType.REMOVE,
                key=key,
                parents=None,
            )
        )

    # 2. Additions
    for key in sorted(diff.added):
        patches.append(
            SignalLineagePatch(
                type=SignalLineagePatchType.ADD,
                key=key,
                parents=None,
            )
        )

    # 3. Moves
    for key in sorted(diff.moved):
        patches.append(
            SignalLineagePatch(
                type=SignalLineagePatchType.MOVE,
                key=key,
                parents=None,
            )
        )

    # 4. Parent rewiring
    for key in sorted(diff.changed_parents):
        patches.append(
            SignalLineagePatch(
                type=SignalLineagePatchType.REWIRE_PARENTS,
                key=key,
                parents=None,
            )
        )

    return tuple(patches)


