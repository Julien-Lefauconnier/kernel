# veramem_kernel/journals/timeline/timeline_signed_commitment.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment, _sha256_hex
from veramem_kernel.ports.signer_port import Signature, SignerPort
from veramem_kernel.common.canonical_encoding import TLV, u64_be, ascii_bytes
from veramem_kernel.common.tlv_schema import MessageSchema, as_ascii, as_bytes, build_message
from veramem_kernel.common.domain_registry import REGISTRY, Domain
from veramem_kernel.journals.timeline.timeline_commitment import _DOMAIN as COMMIT_DOMAIN

_DOMAIN = REGISTRY.register(
    domain=Domain(b"veramem.timeline.signed_commitment.v1"),
    owner="veramem_kernel.journals.timeline.timeline_signed_commitment",
)

_BUNDLE_DOMAIN = REGISTRY.register(
    domain=Domain(b"veramem.timeline.signed_commitment.bundle.v1"),
    owner="veramem_kernel.journals.timeline.timeline_signed_commitment",
)

_BUNDLE_SCHEMA = MessageSchema(
    domain=_BUNDLE_DOMAIN,
    required_tags=(1, 2, 3, 4),
    reject_unknown=True,
)


def _to_message(c: TimelineCommitment) -> bytes:
    # Canonical TLV payload:
    # 1: head (ascii, empty if None)
    # 2: total_entries (u64)
    # 3: timestamp_iso (ascii)
    # 4: commitment (ascii hex)
    head_bytes = ascii_bytes(c.head) if c.head is not None else b""

    return build_message(
        domain=_DOMAIN,
        fields=(
            TLV(1, head_bytes),
            TLV(2, u64_be(c.total_entries)),
            TLV(3, ascii_bytes(c.timestamp_iso)),
            TLV(4, ascii_bytes(c.commitment)),
        ),
    )


@dataclass(frozen=True)
class TimelineSignedCommitment:
    commitment: TimelineCommitment
    signature: Signature

    @classmethod
    def sign(cls, *, commitment: TimelineCommitment, signer: SignerPort) -> "TimelineSignedCommitment":
        msg = _to_message(commitment)
        sig = signer.sign(msg)
        return cls(commitment=commitment, signature=sig)

    def verify(self, *, signer: SignerPort) -> None:
        msg = _to_message(self.commitment)
        signer.verify(msg, self.signature)

    def to_bytes(self) -> bytes:
        msg = _to_message(self.commitment)
        return build_message(
            domain=_BUNDLE_DOMAIN,
            fields=(
                TLV(1, b"\x01"),
                TLV(2, msg),  # embedded canonical message-to-sign bytes
                TLV(3, ascii_bytes(self.signature.algo)),
                TLV(4, ascii_bytes(self.signature.value)),
            ),
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "TimelineSignedCommitment":
        m = _BUNDLE_SCHEMA.parse(raw)
        # strict version
        v = as_bytes(m, 1, ln=1)
        if v != b"\x01":
            raise ValueError("unsupported signed commitment bundle version")

        msg = as_bytes(m, 2)

        if len(msg) > 1_000_000:
            raise ValueError("payload too large")

        algo = as_ascii(m, 3)

        if not algo.isascii():
            raise ValueError("algo must be ASCII")

        if not algo or len(algo) > 32:
            raise ValueError("invalid signature algorithm")

        if not algo.islower():
            raise ValueError("algo must be lowercase canonical")

        if any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for c in algo):
            raise ValueError("invalid algo charset")
        
        _ALLOWED_SIG_ALGOS = {"hmac-sha256", "ed25519"}
        if algo not in _ALLOWED_SIG_ALGOS:
            raise ValueError("unsupported signature algorithm")

        raw_val = as_ascii(m, 4)

        if len(raw_val) != 64:
            raise ValueError("invalid signature length")

        if raw_val != raw_val.lower():
            raise ValueError("signature must be lowercase")

        if any(c not in "0123456789abcdef" for c in raw_val):
            raise ValueError("invalid signature format")

        val = raw_val

        from veramem_kernel.common.canonical_encoding import decode_message
        try:
            dom, tlvs = decode_message(msg)
        except Exception:
            raise ValueError("invalid signed payload")

        if dom != _DOMAIN:
            raise ValueError("signed message domain mismatch")

        tags = {t.tag: bytes(t.value) for t in tlvs}
        if set(tags.keys()) != {1, 2, 3, 4}:
            raise ValueError("signed message schema mismatch")

        # --- head ---
        head_b = tags[1]
        if not head_b.isascii():
            raise ValueError("invalid head encoding")

        head = head_b.decode("ascii") if len(head_b) > 0 else None
        if head is not None:
            if len(head) != 64 or any(c not in "0123456789abcdef" for c in head):
                raise ValueError("invalid head format")

        # --- total ---
        b_total = tags[2]
        if len(b_total) != 8:
            raise ValueError("invalid total_entries encoding")
        total = int.from_bytes(b_total, "big", signed=False)

        # --- timestamp ---
        if not tags[3].isascii():
            raise ValueError("timestamp must be ASCII")
        try:
            ts = tags[3].decode("ascii")
        except Exception:
            raise ValueError("invalid timestamp encoding")
        
        if not ts.isascii() or any(ord(c) < 32 for c in ts):
            raise ValueError("invalid timestamp")
        
        try:
            dt = datetime.fromisoformat(ts)
        except Exception:
            raise ValueError("invalid timestamp")
        
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) != timedelta(0):
            raise ValueError("timestamp must be UTC")
        
        # --- commitment ---
        if not tags[4].isascii():
            raise ValueError("invalid commitment encoding")
        
        commit_hex = tags[4].decode("ascii")

        if len(commit_hex) != 64 or any(c not in "0123456789abcdef" for c in commit_hex):
            raise ValueError("invalid commitment format")
        
        
        # 🔥 recompute canonical commitment
        head_bytes = ascii_bytes(head) if head is not None else b""

        payload = build_message(
            domain=COMMIT_DOMAIN,
            fields=(
                TLV(1, head_bytes),
                TLV(2, u64_be(total)),
                TLV(3, ascii_bytes(ts)),
            ),
        )
        
        _commit_dom = COMMIT_DOMAIN.name if hasattr(COMMIT_DOMAIN, "name") else COMMIT_DOMAIN
        if _commit_dom != b"veramem.timeline.commitment.v1":
            raise ValueError("invalid commitment domain")


        if commit_hex != _sha256_hex(payload):
            raise ValueError("commitment mismatch")

        signature = Signature(algo=algo, value=val)

        expected = TimelineCommitment(
            head=head,
            total_entries=total,
            timestamp_iso=ts,
            commitment=commit_hex,
        )

        return cls(commitment=expected, signature=signature)
