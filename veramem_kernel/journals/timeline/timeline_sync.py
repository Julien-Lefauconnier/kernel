# veramem_kernel/journals/timeline/timeline_sync.py

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from veramem_kernel.common.trust_anchor import TrustAnchor
from veramem_kernel.journals.timeline.timeline_delta import TimelineDelta
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork, TimelineForkKind
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot


class TimelineSyncKind(str, Enum):
    IDENTICAL = "identical"
    LOCAL_NEEDS_REMOTE = "local_needs_remote"   # remote extends local -> apply remote->local delta
    REMOTE_NEEDS_LOCAL = "remote_needs_local"   # local extends remote -> provide local->remote delta
    FORK = "fork"


@dataclass(frozen=True)
class TimelineSyncResult:
    kind: TimelineSyncKind
    fork: TimelineFork
    delta: TimelineDelta | None = None

    def is_fork(self) -> bool:
        return self.kind == TimelineSyncKind.FORK


class TimelineSyncError(ValueError):
    pass


class TimelineSync:
    """
    Pure kernel sync decision engine.

    - No I/O
    - Deterministic
    - Uses TrustAnchor for anti-rollback
    - Uses TimelineFork to classify relationship
    - Uses TimelineDelta for linear fast path
    """

    @staticmethod
    def sync(
        *,
        local: TimelineSnapshot,
        remote: TimelineSnapshot,
        anchor: TrustAnchor,
    ) -> TimelineSyncResult:
        """
        Decide what to do when syncing `local` with `remote`.
        """

        # Anti-rollback checks: both must be >= anchor
        anchor.verify(local.cursor())
        anchor.verify(remote.cursor())

        fork = TimelineFork.detect(local, remote)
        fork.assert_consistent()

        if fork.kind == TimelineForkKind.IDENTICAL:
            return TimelineSyncResult(
                kind=TimelineSyncKind.IDENTICAL,
                fork=fork,
                delta=None,
            )

        # Remote extends local: build delta to bring local up to remote
        if fork.kind == TimelineForkKind.EXTENDS_LEFT:
            delta = TimelineDelta(
                base=local.cursor(),
                target=remote.cursor(),
                entries=remote.entries[fork.common_prefix_len :],
            )
            return TimelineSyncResult(
                kind=TimelineSyncKind.LOCAL_NEEDS_REMOTE,
                fork=fork,
                delta=delta,
            )

        # Local extends remote: build delta to bring remote up to local
        if fork.kind == TimelineForkKind.EXTENDS_RIGHT:
            delta = TimelineDelta(
                base=remote.cursor(),
                target=local.cursor(),
                entries=local.entries[fork.common_prefix_len :],
            )
            return TimelineSyncResult(
                kind=TimelineSyncKind.REMOTE_NEEDS_LOCAL,
                fork=fork,
                delta=delta,
            )

        # True fork: cannot reconcile at kernel level
        return TimelineSyncResult(
            kind=TimelineSyncKind.FORK,
            fork=fork,
            delta=None,
        )

    @staticmethod
    def apply_local_update(
        *,
        local: TimelineSnapshot,
        result: TimelineSyncResult,
        anchor: TrustAnchor,
    ) -> tuple[TimelineSnapshot, TrustAnchor]:
        """
        Apply the sync result to the local snapshot when appropriate.
        Only valid for LOCAL_NEEDS_REMOTE with a delta.
        """
        if result.kind != TimelineSyncKind.LOCAL_NEEDS_REMOTE or result.delta is None:
            raise TimelineSyncError("no applicable delta for local update")

        # apply delta (will verify base + target cursor)
        updated = result.delta.apply_to(local)

        # advance anchor to the new state
        new_anchor = anchor.advance(updated.cursor())
        return updated, new_anchor
