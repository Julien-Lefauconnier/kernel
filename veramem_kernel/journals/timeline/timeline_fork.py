# veramem_kernel/journals/timeline/timeline_fork.py

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, List

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.common.canonical_encoding import encode_message, decode_message, TLV, ascii_bytes, u64_be



class TimelineForkError(ValueError):
    pass

class TimelineForkDecodeError(TimelineForkError):
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
            raise TimelineForkDecodeError("truncated frame length")
        ln = int.from_bytes(blob[i:i+4], "big")
        i += 4
        if i + ln > n:
            raise TimelineForkDecodeError("invalid frame length")
        out.append(blob[i:i+ln])
        i += ln
    if i != n:
        raise TimelineForkDecodeError("extra bytes after frames")
    return out

def _decode_head(value: bytes | None) -> str | None:
    if value is None:
        return None
    try:
        s = value.decode("ascii")
    except Exception:
        raise TimelineForkDecodeError("head must be ASCII")
    
    if len(s) != 64 or any(c not in "0123456789abcdef" for c in s):
        raise TimelineForkDecodeError("invalid head format")
    return s

class TimelineForkKind(str, Enum):
    """
    Classification of relationship between two snapshots.
    """
    IDENTICAL = "identical"
    EXTENDS_LEFT = "extends_left"    # right extends left (left is prefix of right)
    EXTENDS_RIGHT = "extends_right"  # left extends right (right is prefix of left)
    FORK = "fork"


@dataclass(frozen=True)
class TimelineFork:
    """
    Deterministic fork descriptor between two TimelineSnapshots.

    This is a *pure* kernel primitive: it only describes the divergence.
    Reconciliation/merge is handled by higher layers (policy / authority).
    """

    kind: TimelineForkKind
    common_prefix_len: int

    left_head: str | None
    right_head: str | None

    left_total_entries: int
    right_total_entries: int

    # Suffixes after the common prefix (may be empty in extension cases)
    left_suffix: Tuple[TimelineEntry, ...]
    right_suffix: Tuple[TimelineEntry, ...]

    @classmethod
    def detect(cls, left: TimelineSnapshot, right: TimelineSnapshot) -> "TimelineFork":
        le = left.entries
        re = right.entries

        min_len = min(len(le), len(re))
        k = 0
        while k < min_len and le[k] == re[k]:
            k += 1

        if k == len(le) == len(re):
            kind = TimelineForkKind.IDENTICAL
        elif k == len(le) and len(le) < len(re):
            kind = TimelineForkKind.EXTENDS_LEFT
        elif k == len(re) and len(re) < len(le):
            kind = TimelineForkKind.EXTENDS_RIGHT
        else:
            kind = TimelineForkKind.FORK

        out = cls(
            kind=kind,
            common_prefix_len=k,
            left_head=left.head,
            right_head=right.head,
            left_total_entries=len(le),
            right_total_entries=len(re),
            left_suffix=tuple(le[k:]),
            right_suffix=tuple(re[k:]),
        )

        out.assert_consistent()
        return out


    def is_fork(self) -> bool:
        return self.kind == TimelineForkKind.FORK

    def assert_consistent(self) -> None:
        """
        Kernel sanity checks (internal invariants of this structure).
        """
        if self.common_prefix_len < 0:
            raise TimelineForkError("common_prefix_len must be >= 0")

        if self.common_prefix_len > self.left_total_entries:
            raise TimelineForkError("common_prefix_len exceeds left length")

        if self.common_prefix_len > self.right_total_entries:
            raise TimelineForkError("common_prefix_len exceeds right length")

        if len(self.left_suffix) != (self.left_total_entries - self.common_prefix_len):
            raise TimelineForkError("left_suffix length mismatch")

        if len(self.right_suffix) != (self.right_total_entries - self.common_prefix_len):
            raise TimelineForkError("right_suffix length mismatch")
        
        if self.left_total_entries < 0 or self.right_total_entries < 0:
            raise TimelineForkError("invalid total entries")


    def to_bytes(self) -> bytes:
        fields = [
            TLV(1, b"\x01"),
            TLV(2, ascii_bytes(self.kind.value)),
            TLV(3, u64_be(self.common_prefix_len)),
            TLV(6, u64_be(self.left_total_entries)),
            TLV(7, u64_be(self.right_total_entries)),
            TLV(8, _pack_frames([e.to_bytes() for e in self.left_suffix])),
            TLV(9, _pack_frames([e.to_bytes() for e in self.right_suffix])),
        ]

        if self.left_head is not None:
            fields.append(TLV(4, ascii_bytes(self.left_head)))

        if self.right_head is not None:
            fields.append(TLV(5, ascii_bytes(self.right_head)))

        # ⚠️ tags strictement croissants => on trie
        fields = sorted(fields, key=lambda t: t.tag)

        return encode_message(
            domain=b"veramem.timeline.fork.v1",
            fields=tuple(fields),
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineFork":
        dom, tlvs = decode_message(raw)
        if dom != b"veramem.timeline.fork.v1":
            raise TimelineForkDecodeError("invalid domain for timeline fork")

        m = {t.tag: t.value for t in tlvs}

        # --- strict version ---
        if 1 not in m:
            raise TimelineForkDecodeError("missing fork wire version")
        if m[1] != b"\x01":
            raise TimelineForkDecodeError("unsupported fork wire version")

        # --- required fields ---
        for tag in (2, 3, 6, 7, 8, 9):
            if tag not in m:
                raise TimelineForkDecodeError(f"missing fork field: {tag}")

        try:
            kind_b = m[2].decode("ascii")
        except Exception:
            raise TimelineForkDecodeError("invalid fork kind encoding")

        try:
            kind = TimelineForkKind(kind_b)
        except ValueError:
            raise TimelineForkDecodeError("invalid fork kind")

        common_prefix_len = int.from_bytes(m[3], "big")

        left_head = _decode_head(m.get(4))
        right_head = _decode_head(m.get(5))

        left_total = int.from_bytes(m[6], "big")
        right_total = int.from_bytes(m[7], "big")

        if len(m[8]) > 50_000_000 or len(m[9]) > 50_000_000:
            raise TimelineForkDecodeError("suffix blob too large")
        
        if len(m) > 20:
            raise TimelineForkDecodeError("too many fields")

        left_suffix = tuple(TimelineEntry.from_bytes(b) for b in _unpack_frames(m[8]))
        right_suffix = tuple(TimelineEntry.from_bytes(b) for b in _unpack_frames(m[9]))

        if len(left_suffix) != (left_total - common_prefix_len):
            raise TimelineForkDecodeError("left suffix mismatch")
        
        if len(right_suffix) != (right_total - common_prefix_len):
            raise TimelineForkDecodeError("right suffix mismatch")
        
        if len(left_suffix) > 10_000:
            raise TimelineForkDecodeError("suffix too large")
        
        if len(right_suffix) > 10_000:
            raise TimelineForkDecodeError("suffix too large")
        
        if left_total > 1_000_000 or right_total > 1_000_000:
            raise TimelineForkDecodeError("snapshot too large")
        
        
        
        if common_prefix_len > left_total or common_prefix_len > right_total:
            raise TimelineForkDecodeError("invalid prefix")

        out = cls(
            kind=kind,
            common_prefix_len=common_prefix_len,
            left_head=left_head,
            right_head=right_head,
            left_total_entries=left_total,
            right_total_entries=right_total,
            left_suffix=left_suffix,
            right_suffix=right_suffix,
        )
        out.assert_consistent()
        return out
