# veramem_kernel/common/trust_anchor.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor


class TrustAnchorError(ValueError):
    pass


class RollbackDetected(TrustAnchorError):
    """
    Raised when a proposed cursor is older than the trusted anchor.
    """


@dataclass(frozen=True)
class TrustAnchor:
    """
    Minimal anti-rollback primitive.

    The anchor stores the strongest known cursor.
    It enforces monotonic progression.
    """

    best: Optional[TimelineCursor] = None

    def verify(self, candidate: TimelineCursor) -> None:
        """
        Check that the candidate does not rollback the state.
        """

        if self.best is None:
            return

        # Reject smaller timeline
        if candidate.total_entries < self.best.total_entries:
            raise RollbackDetected(
                "rollback detected: fewer entries than trusted state"
            )

        # Same length but different head = fork attack or corruption
        if (
            candidate.total_entries == self.best.total_entries
            and candidate.head != self.best.head
        ):
            raise RollbackDetected(
                "rollback detected: conflicting head at same height"
            )

    def advance(self, candidate: TimelineCursor) -> "TrustAnchor":
        """
        Update anchor if candidate is strictly stronger.
        """

        self.verify(candidate)

        if self.best is None:
            return TrustAnchor(best=candidate)

        if candidate.total_entries > self.best.total_entries:
            return TrustAnchor(best=candidate)

        # Same or weaker -> unchanged
        return self
