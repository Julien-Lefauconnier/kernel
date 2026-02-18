# veramem_kernel/journals/timeline/timeline_delta.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict
from typing import Tuple, List

from veramem_kernel.common.canonical_encoding import encode_message, decode_message, TLV
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry
from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot


# ============================================================
# Errors
# ============================================================

class TimelineDeltaError(ValueError):
    pass


class TimelineDeltaBaseMismatch(TimelineDeltaError):
    pass


class TimelineDeltaTargetMismatch(TimelineDeltaError):
    pass


class TimelineDeltaEmptyError(TimelineDeltaError):
    pass


class TimelineDeltaDecodeError(TimelineDeltaError):
    pass


# ============================================================
# helpers: framing
# ============================================================

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
            raise TimelineDeltaDecodeError("truncated frame length")
        ln = int.from_bytes(blob[i:i+4], "big")
        i += 4
        if ln < 0 or i + ln > n:
            raise TimelineDeltaDecodeError("invalid frame length")
        out.append(blob[i:i+ln])
        i += ln
    if i != n:
        raise TimelineDeltaDecodeError("extra bytes after frames")
    return out


# ============================================================
# TimelineDelta
# ============================================================

@dataclass(frozen=True)
class TimelineDelta:
    """
    Immutable append-only delta.

    Guarantees:
    - deterministic replay
    - append-only
    - distributed sync safe
    - rollback detection
    """

    base: TimelineCursor
    target: TimelineCursor
    entries: Tuple[TimelineEntry, ...]

    def __post_init__(self) -> None:
        if self.entries is None:
            raise TimelineDeltaError("entries must not be None")
        if len(self.entries) == 0:
            raise TimelineDeltaEmptyError("timeline delta cannot be empty")
        if self.base.total_entries + len(self.entries) != self.target.total_entries:
            raise TimelineDeltaError("delta length mismatch with target cursor")
        
        ids = [e.entry_id for e in self.entries]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate entries in delta")


    # --------------------------------------------------
    # Core apply
    # --------------------------------------------------
    def apply_to(self, snap: TimelineSnapshot) -> TimelineSnapshot:
        if snap.cursor() != self.base:
            raise TimelineDeltaBaseMismatch("snapshot cursor does not match delta base")

        out = snap
        for e in self.entries:
            out = out.append(e)

        cursor = out.cursor()
        if cursor != self.target:
            raise TimelineDeltaTargetMismatch("resulting snapshot cursor does not match delta target")
        return out

    # --------------------------------------------------
    # Verification
    # --------------------------------------------------
    def verify_against(self, snap: TimelineSnapshot) -> None:
        if snap.cursor() != self.base:
            raise TimelineDeltaBaseMismatch("snapshot cursor mismatch during verification")


    # --------------------------------------------------
    # Builders
    # --------------------------------------------------
    @classmethod
    def from_snapshots(
        cls,
        base: TimelineSnapshot,
        target: TimelineSnapshot,
    ) -> "TimelineDelta":
        """
        Build an append-only delta between two snapshots.

        Guarantees:
        - deterministic
        - append-only
        - rollback detection
        """

        base_cursor = base.cursor()
        target_cursor = target.cursor()

        # --- no rollback ---
        if target_cursor.total_entries < base_cursor.total_entries:
            raise TimelineDeltaError("target snapshot is older than base")

        # --- trivial mismatch ---
        if target_cursor.total_entries == base_cursor.total_entries:
            raise TimelineDeltaEmptyError("no delta between identical snapshots")

        # --- extract appended entries ---
        start = base_cursor.total_entries
        end = target_cursor.total_entries

        try:
            new_entries = target.entries[start:end]
        except Exception as e:
            raise TimelineDeltaError("cannot extract delta entries") from e

        if len(new_entries) == 0:
            raise TimelineDeltaEmptyError("delta extraction failed")

        return cls(
            base=base_cursor,
            target=target_cursor,
            entries=tuple(new_entries),
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------
    def size(self) -> int:
        return len(self.entries)

    # --------------------------------------------------
    # Canonical bytes
    # --------------------------------------------------
    def to_bytes(self) -> bytes:
        base_b = self.base.to_bytes()
        target_b = self.target.to_bytes()
        entries_b = _pack_frames([e.to_bytes() for e in self.entries])

        return encode_message(
            domain=b"veramem.timeline.delta.v1",
            fields=(
                # tag 1: protocol version (wire)
                TLV(1, b"\x01"),
                TLV(2, base_b),
                TLV(3, target_b),
                TLV(4, entries_b),
            ),
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineDelta":
        dom, tlvs = decode_message(raw)
        if dom != b"veramem.timeline.delta.v1":
            raise TimelineDeltaDecodeError("invalid domain for timeline delta")

        fields: Dict[int, bytes] = {t.tag: t.value for t in tlvs}

        if 1 not in fields:
            raise TimelineDeltaDecodeError("missing timeline delta wire version")
        if fields[1] != b"\x01":
            raise TimelineDeltaDecodeError("unsupported timeline delta wire version")

        try:
            base_b = fields[2]
            target_b = fields[3]
            entries_b = fields[4]
        except KeyError as e:
            raise TimelineDeltaDecodeError(f"missing field: {e}") from e

        base = TimelineCursor.from_bytes(base_b)
        target = TimelineCursor.from_bytes(target_b)

        entry_frames = _unpack_frames(entries_b)
        entries = tuple(TimelineEntry.from_bytes(b) for b in entry_frames)

        return cls(base=base, target=target, entries=entries)
