# veramem_kernel/journals/timeline/timeline_merge.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from enum import Enum
from typing import Dict, List, Tuple

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_fork import TimelineFork
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.common.canonical_encoding import encode_message, decode_message, TLV, ascii_bytes, u64_be


class TimelineMergeError(ValueError):
    pass

class TimelineMergeDecodeError(TimelineMergeError):
    pass


def _pack_frames(frames: List[bytes]) -> bytes:
    out = bytearray()
    for f in frames:
        out += len(f).to_bytes(4, "big")
        out += f
    return bytes(out)


def _unpack_frames(blob: bytes) -> List[bytes]:
    out: List[bytes] = []
    i = 0
    n = len(blob)
    while i < n:
        if i + 4 > n:
            raise TimelineMergeDecodeError("truncated frame length")
        ln = int.from_bytes(blob[i:i+4], "big")
        i += 4
        if i + ln > n:
            raise TimelineMergeDecodeError("invalid frame length")
        out.append(blob[i:i+ln])
        i += ln
    if i != n:
        raise TimelineMergeDecodeError("extra bytes after frames")
    return out


class TimelineMergeKind(str, Enum):
    MERGED = "merged"
    NO_MERGE = "no_merge"


class TimelineMergeConflict(TimelineMergeError):
    """
    Raised when two branches cannot be deterministically merged
    without losing information or breaking invariants.
    """


@dataclass(frozen=True)
class TimelineMergeResult:
    kind: TimelineMergeKind
    merged: TimelineSnapshot | None = None
    reason: str | None = None

    def to_bytes(self) -> bytes:
        fields = [
            TLV(1, b"\x01"),
            TLV(2, ascii_bytes(self.kind.value)),
        ]

        if self.reason is not None:
            fields.append(TLV(3, ascii_bytes(self.reason)))

        if self.merged is not None:
            fields.append(TLV(4, u64_be(len(self.merged.entries))))
            fields.append(TLV(5, _pack_frames([e.to_bytes() for e in self.merged.entries])))
            if self.merged.head is not None:
                fields.append(TLV(6, ascii_bytes(self.merged.head)))


        fields = sorted(fields, key=lambda t: t.tag)

        return encode_message(
            domain=b"veramem.timeline.merge_result.v1",
            fields=tuple(fields),
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineMergeResult":
        dom, tlvs = decode_message(raw)
        if dom != b"veramem.timeline.merge_result.v1":
            raise TimelineMergeDecodeError("invalid domain for merge result")

        m: Dict[int, bytes] = {t.tag: t.value for t in tlvs}

        if 1 not in m:
            raise TimelineMergeDecodeError("missing merge result wire version")
        if m[1] != b"\x01":
            raise TimelineMergeDecodeError("unsupported merge result wire version")

        kind = TimelineMergeKind(m[2].decode("ascii"))
        reason = m.get(3).decode("ascii") if 3 in m else None

        merged = None

        if 5 in m:
            frames = _unpack_frames(m[5])
            entries = tuple(TimelineEntry.from_bytes(b) for b in frames)
            merged = TimelineSnapshot.build(entries)

            # restore head if present
            if 6 in m:
                head = m[6].decode("ascii")
                if merged.head != head:
                    raise TimelineMergeDecodeError(
                        "merge head mismatch (possible tampering)"
                    )

        return cls(kind=kind, merged=merged, reason=reason)



class TimelineMerge:
    """
    Deterministic merge of two forked timelines.

    Conservative rules:
    - never modify the common prefix
    - merge only suffixes
    - deterministic ordering for interleaving
    - reject entry_id collisions in suffixes
    """

    @staticmethod
    def try_merge(
        *,
        fork: TimelineFork,
        local: TimelineSnapshot,
        remote: TimelineSnapshot,
    ) -> TimelineMergeResult:
        if not fork.is_fork():
            # Not a fork: merging is unnecessary; caller should use TimelineDelta.
            return TimelineMergeResult(kind=TimelineMergeKind.NO_MERGE, reason="not_a_fork")

        k = fork.common_prefix_len

        # Common prefix must be identical by construction of TimelineFork
        prefix = local.entries[:k]

        left_suffix = list(local.entries[k:])
        right_suffix = list(remote.entries[k:])

        # Reject entry_id collisions across suffixes (conflict)
        left_ids = {e.entry_id for e in left_suffix}
        right_ids = {e.entry_id for e in right_suffix}

        if left_ids.intersection(right_ids):
            return TimelineMergeResult(
                kind=TimelineMergeKind.NO_MERGE,
                reason="entry_id_collision_in_suffix",
            )

        # Deterministic interleave order:
        # deterministic causal ordering
        # entry_id ascending (stable tie-breaker)
        merged_suffix = left_suffix + right_suffix
        merged_suffix.sort(key=lambda e: (e.lamport, e.device_id, e.entry_id))

        # Build merged snapshot
        merged_entries: Tuple[TimelineEntry, ...] = tuple(prefix) + tuple(merged_suffix)
        merged = TimelineSnapshot.build(merged_entries)

        return TimelineMergeResult(kind=TimelineMergeKind.MERGED, merged=merged)

    
