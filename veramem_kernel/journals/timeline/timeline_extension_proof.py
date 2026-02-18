# veramem_kernel/journals/timeline/timeline_extension_proof.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment


@dataclass(frozen=True)
class TimelineExtensionProof:
    """
    Proof that `target` snapshot is a deterministic extension of `base`.

    v1: includes delta entries (full proof).
    v2+: can be upgraded to Merkle witnesses for partial disclosure.
    """

    base: TimelineCursor
    target: TimelineCommitment
    entries: Tuple[TimelineEntry, ...]

    @classmethod
    def build(cls, *, base: TimelineSnapshot, target: TimelineSnapshot) -> "TimelineExtensionProof":
        # Build delta entries only if target extends base
        bcur = base.cursor()
        tcur = target.cursor()

        if tcur.total_entries < bcur.total_entries:
            raise ValueError("target cannot be shorter than base")

        # Check prefix match by position
        prefix = target.entries[: bcur.total_entries]
        if prefix != base.entries:
            raise ValueError("target is not an extension of base")

        delta_entries = target.entries[bcur.total_entries :]

        return cls(
            base=bcur,
            target=TimelineCommitment.from_snapshot(target),
            entries=tuple(delta_entries),
        )

    def verify_and_apply(self, base_snap: TimelineSnapshot) -> TimelineSnapshot:
        """
        Verifies proof against base snapshot, applies delta, and verifies final commitment.
        """

        if base_snap.cursor() != self.base:
            raise ValueError("base cursor mismatch")

        # Replay delta WITHOUT reconstructing a fake target cursor
        updated = base_snap
        for e in self.entries:
            updated = updated.append(e)

        # Now verify the final commitment
        self.target.verify_against(updated)

        return updated

