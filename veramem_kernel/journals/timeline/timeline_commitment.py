# veramem_kernel/journals/timeline/timeline_commitment.py

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from veramem_kernel.journals.timeline.timeline_cursor import TimelineCursor
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.common.canonical_encoding import TLV, u64_be, ascii_bytes
from veramem_kernel.common.domain_registry import REGISTRY, Domain
from veramem_kernel.common.tlv_schema import MessageSchema, TlvSchemaError, as_ascii, as_u64, as_bytes, build_message

_DOMAIN = REGISTRY.register(
    domain=Domain(b"veramem.timeline.commitment.v1"),
    owner="veramem_kernel.journals.timeline.timeline_commitment",
)

_SCHEMA = MessageSchema(
    domain=_DOMAIN,
    required_tags=(1, 2, 3),
    allow_empty=(1,),  # head may be empty when None
    reject_unknown=True,
)

def _sha256_hex(data: bytes) -> str:
    return sha256(data).hexdigest()


@dataclass(frozen=True)
class TimelineCommitment:
    """
    Compact, domain-separated cryptographic commitment to a timeline state.

    This is NOT a signature. It is a stable commitment that can be signed later.
    """

    head: str | None
    total_entries: int
    timestamp_iso: str
    commitment: str

    @classmethod
    def from_snapshot(cls, snap: TimelineSnapshot) -> "TimelineCommitment":
        cur: TimelineCursor = snap.cursor()

        head = cur.head
        total = cur.total_entries
        ts_iso = cur.timestamp.isoformat()

        # Canonical TLV payload:
        # 1: head (ascii, empty if None)
        # 2: total_entries (u64)
        # 3: timestamp_iso (ascii)
        head_bytes = ascii_bytes(head) if head is not None else b""

        payload = build_message(
            domain=_DOMAIN,
            fields=(TLV(1, head_bytes), TLV(2, u64_be(total)), TLV(3, ascii_bytes(ts_iso))),
        )

        return cls(
            head=head,
            total_entries=total,
            timestamp_iso=ts_iso,
            commitment=_sha256_hex(payload),
        )

    def verify_against(self, snap: TimelineSnapshot) -> None:
        other = TimelineCommitment.from_snapshot(snap)
        if other != self:
            raise ValueError("TimelineCommitment mismatch")

    def to_bytes(self) -> bytes:
        head_bytes = ascii_bytes(self.head) if self.head is not None else b""
        msg = build_message(
            domain=_DOMAIN,
            fields=(
                TLV(1, head_bytes),
                TLV(2, u64_be(self.total_entries)),
                TLV(3, ascii_bytes(self.timestamp_iso)),
            ),
        )
        return msg

    @classmethod
    def from_bytes(cls, msg: bytes) -> "TimelineCommitment":
        m = _SCHEMA.parse(msg)
        head_raw = as_bytes(m, 1)
        
        head = as_ascii(m, 1) if len(head_raw) > 0 else None
        if head is not None:
            if len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
                raise ValueError("invalid head format")
        total = as_u64(m, 2)
        ts = as_ascii(m, 3)

        # --- strict timestamp validation ---
        if not ts.isascii() or any(ord(c) < 32 for c in ts):
            raise ValueError("invalid timestamp encoding")

        # ensure ISO-8601 + UTC
        from datetime import datetime, timedelta
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) != timedelta(0):
            raise ValueError("timestamp must be UTC ISO8601")

        # commitment is always derived from canonical bytes
        out = cls(
            head=head,
            total_entries=int(total),
            timestamp_iso=ts,
            commitment=_sha256_hex(bytes(msg)),
        )

        if len(out.commitment) != 64:
            raise ValueError("invalid commitment length")

        return out
