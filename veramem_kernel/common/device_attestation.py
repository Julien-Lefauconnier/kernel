# veramem_kernel/common/device_attestation.py

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from veramem_kernel.ports.signer_port import Signature, SignerPort
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.common.canonical_encoding import TLV, ascii_bytes
from veramem_kernel.ports.challenge_store_port import ChallengeRecord, ChallengeStorePort
from veramem_kernel.common.domain_registry import REGISTRY, Domain
from veramem_kernel.common.tlv_schema import MessageSchema, as_ascii, as_bytes, build_message


_DOMAIN = REGISTRY.register(
    domain=Domain(b"veramem.device.attestation.v1"),
    owner="veramem_kernel.common.device_attestation",
)

_BUNDLE_DOMAIN = REGISTRY.register(
    domain=Domain(b"veramem.device.attestation.bundle.v1"),
    owner="veramem_kernel.common.device_attestation",
)

# Bundle schema MUST match interop tests:
# 1: signed_commitment bundle bytes
# 2: challenge_hash (32 bytes)
# 3: response.algo (ascii)
# 4: response.value (ascii hex)
_BUNDLE_SCHEMA = MessageSchema(
    domain=_BUNDLE_DOMAIN,
    required_tags=(1, 2, 3, 4),
    reject_unknown=True,
)


def _hash_challenge(challenge: bytes) -> bytes:
    return sha256(challenge).digest()


def _to_payload(*, signed: TimelineSignedCommitment, challenge_hash: bytes) -> bytes:
    # Canonical TLV payload (matches interop tests):
    # 1: signed_commitment.signature.algo (ascii)
    # 2: signed_commitment.signature.value (ascii hex)
    # 3: challenge_hash (raw 32 bytes)
    return build_message(
        domain=_DOMAIN,
        fields=(
            TLV(1, ascii_bytes(signed.signature.algo)),
            TLV(2, ascii_bytes(signed.signature.value)),
            TLV(3, bytes(challenge_hash)),
        ),
    )


@dataclass(frozen=True)
class DeviceAttestation:
    signed_commitment: TimelineSignedCommitment
    challenge_hash_hex: str
    response: Signature

    @classmethod
    def respond(
        cls,
        *,
        signed_commitment: TimelineSignedCommitment,
        signer: SignerPort,
        challenge: bytes,
    ) -> "DeviceAttestation":
        ch = _hash_challenge(challenge)
        payload = _to_payload(signed=signed_commitment, challenge_hash=ch)
        resp = signer.sign(payload)
        return cls(
            signed_commitment=signed_commitment,
            challenge_hash_hex=ch.hex(),
            response=resp,
        )

    def verify(self, *, signer: SignerPort, challenge: bytes) -> None:
        # verify signed commitment itself
        self.signed_commitment.verify(signer=signer)

        ch = _hash_challenge(challenge)
        if ch.hex() != self.challenge_hash_hex:
            raise ValueError("challenge mismatch")

        payload = _to_payload(signed=self.signed_commitment, challenge_hash=ch)
        signer.verify(payload, self.response)

    def verify_with_store(
        self,
        *,
        signer: SignerPort,
        challenge: bytes,
        store: ChallengeStorePort,
    ) -> None:
        # 1) verify first (no side effects)
        self.verify(signer=signer, challenge=challenge)

        # 2) mark used only after successful verification
        record = ChallengeRecord(challenge_hash_hex=self.challenge_hash_hex)
        store.mark_used(record)

    def to_bytes(self) -> bytes:
        signed_bytes = self.signed_commitment.to_bytes()
        return build_message(
            domain=_BUNDLE_DOMAIN,
            fields=(
                TLV(1, signed_bytes),
                TLV(2, bytes.fromhex(self.challenge_hash_hex)),
                TLV(3, ascii_bytes(self.response.algo)),
                TLV(4, ascii_bytes(self.response.value)),
            ),
        )

    @classmethod
    def from_bytes(cls, raw: bytes) -> "DeviceAttestation":
        m = _BUNDLE_SCHEMA.parse(raw)

        signed_raw = as_bytes(m, 1)
        ch = as_bytes(m, 2, ln=32)
        algo = as_ascii(m, 3)
        val = as_ascii(m, 4)

        signed = TimelineSignedCommitment.from_bytes(signed_raw)
        resp = Signature(algo=algo, value=val)

        return cls(
            signed_commitment=signed,
            challenge_hash_hex=ch.hex(),
            response=resp,
        )
