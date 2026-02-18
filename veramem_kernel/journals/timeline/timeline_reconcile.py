# veramem_kernel/journals/timeline/timeline_reconcile.py

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.common.canonical_encoding import encode_message, decode_message, TLV, ascii_bytes, u64_be



class ReconcileDecisionKind(str, Enum):
    KEEP_LOCAL = "keep_local"
    KEEP_REMOTE = "keep_remote"
    KEEP_BOTH = "keep_both"  # export both branches (no merge)


class TimelineReconcileError(ValueError):
    pass

class TimelineReconcileDecodeError(TimelineReconcileError):
    pass

@dataclass(frozen=True)
class TimelineReconcileDecision:
    """
    Deterministic representation of a reconciliation choice.
    """

    kind: ReconcileDecisionKind

    # Minimal traceability fields
    local_head: str | None
    remote_head: str | None
    common_prefix_len: int

    @classmethod
    def from_fork_keep_local(cls, fork: TimelineFork) -> "TimelineReconcileDecision":
        return cls(
            kind=ReconcileDecisionKind.KEEP_LOCAL,
            local_head=fork.left_head,
            remote_head=fork.right_head,
            common_prefix_len=fork.common_prefix_len,
        )

    @classmethod
    def from_fork_keep_remote(cls, fork: TimelineFork) -> "TimelineReconcileDecision":
        return cls(
            kind=ReconcileDecisionKind.KEEP_REMOTE,
            local_head=fork.left_head,
            remote_head=fork.right_head,
            common_prefix_len=fork.common_prefix_len,
        )

    @classmethod
    def from_fork_keep_both(cls, fork: TimelineFork) -> "TimelineReconcileDecision":
        return cls(
            kind=ReconcileDecisionKind.KEEP_BOTH,
            local_head=fork.left_head,
            remote_head=fork.right_head,
            common_prefix_len=fork.common_prefix_len,
        )
    
    def to_bytes(self) -> bytes:
        fields = [
            TLV(1, b"\x01"),
            TLV(2, ascii_bytes(self.kind.value)),
            TLV(3, u64_be(self.common_prefix_len)),
        ]
        if self.local_head is not None:
            fields.append(TLV(4, ascii_bytes(self.local_head)))
        if self.remote_head is not None:
            fields.append(TLV(5, ascii_bytes(self.remote_head)))

        fields = sorted(fields, key=lambda t: t.tag)

        return encode_message(
            domain=b"veramem.timeline.reconcile_decision.v1",
            fields=tuple(fields),
        )

    def assert_consistent(self) -> None:
        if self.common_prefix_len < 0:
            raise TimelineReconcileError("invalid prefix length")

        if self.local_head is not None and len(self.local_head) != 64:
            raise TimelineReconcileError("invalid local head")

        if self.remote_head is not None and len(self.remote_head) != 64:
            raise TimelineReconcileError("invalid remote head")

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineReconcileDecision":
        dom, tlvs = decode_message(raw)
        if dom != b"veramem.timeline.reconcile_decision.v1":
            raise TimelineReconcileDecodeError("invalid domain for reconcile decision")

        m = {t.tag: t.value for t in tlvs}

        # strict version
        if 1 not in m:
            raise TimelineReconcileDecodeError("missing version")
        if m[1] != b"\x01":
            raise TimelineReconcileDecodeError("unsupported version")

        if 2 not in m or 3 not in m:
            raise TimelineReconcileDecodeError("missing required fields")

        kind = ReconcileDecisionKind(m[2].decode("ascii"))
        common_prefix_len = int.from_bytes(m[3], "big")

        local_head = m.get(4).decode("ascii") if 4 in m else None

        if local_head is not None:
            if any(c not in "0123456789abcdef" for c in local_head):
                raise TimelineReconcileDecodeError("invalid local head format")
            if len(local_head) != 64:
                raise TimelineReconcileDecodeError("invalid local head length")

        
        remote_head = m.get(5).decode("ascii") if 5 in m else None

        if remote_head is not None:
            if any(c not in "0123456789abcdef" for c in remote_head):
                raise TimelineReconcileDecodeError("invalid remote head format")
            if len(remote_head) != 64:
                raise TimelineReconcileDecodeError("invalid remote head length")


        decision = cls(
            kind=kind,
            local_head=local_head,
            remote_head=remote_head,
            common_prefix_len=common_prefix_len,
        )

        decision.assert_consistent()
        return decision



@dataclass(frozen=True)
class TimelineReconcileResult:
    """
    Outcome of applying a reconcile decision.
    """

    kind: ReconcileDecisionKind
    primary: TimelineSnapshot
    secondary: TimelineSnapshot | None = None


class TimelineReconcile:
    """
    Apply reconciliation choices to two snapshots.
    """

    @staticmethod
    def apply(
        *,
        fork: TimelineFork,
        local: TimelineSnapshot,
        remote: TimelineSnapshot,
        decision: TimelineReconcileDecision,
    ) -> TimelineReconcileResult:
        # sanity checks: decision matches fork heads
        if decision.local_head != fork.left_head or decision.remote_head != fork.right_head:
            raise TimelineReconcileError("decision does not match fork heads")

        if decision.common_prefix_len != fork.common_prefix_len:
            raise TimelineReconcileError("decision does not match fork prefix length")

        if decision.kind == ReconcileDecisionKind.KEEP_LOCAL:
            return TimelineReconcileResult(kind=decision.kind, primary=local, secondary=None)

        if decision.kind == ReconcileDecisionKind.KEEP_REMOTE:
            return TimelineReconcileResult(kind=decision.kind, primary=remote, secondary=None)

        if decision.kind == ReconcileDecisionKind.KEEP_BOTH:
            # export both branches: local as primary, remote as secondary (deterministic ordering)
            return TimelineReconcileResult(kind=decision.kind, primary=local, secondary=remote)

        raise TimelineReconcileError("unknown reconcile decision kind")

    

