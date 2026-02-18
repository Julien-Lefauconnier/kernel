# tests/test_device_attestation_interop_kernel.py

from hashlib import sha256
import pytest

from veramem_kernel.common.canonical_encoding import decode_message
from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from tests.test_device_attestation_bytes_kernel import _entry
from veramem_kernel.ports.signer_port import Signature


def test_device_attestation_interop():
    """
    Third-party verification of a Veramem device attestation.

    This test intentionally uses ONLY:
    - canonical TLV decoding
    - SHA-256
    - signature verification

    No kernel validation helpers are used.

    This demonstrates that the Veramem kernel format is:
    - deterministic
    - auditable
    - independently verifiable by external systems.
    """

    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    commitment = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=commitment, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = att.to_bytes()

    # =====================================================
    # Step 1 — Parse attestation bundle
    # =====================================================
    dom, tlvs = decode_message(raw)
    assert dom == b"veramem.device.attestation.bundle.v1"

    fields = {t.tag: t.value for t in tlvs}

    signed_bytes = fields[1]
    challenge_hash = fields[2]
    att_algo = fields[3].decode("ascii")
    att_signature = fields[4].decode("ascii")

    # =====================================================
    # Step 2 — Parse signed commitment bundle
    # =====================================================
    dom2, tlvs2 = decode_message(signed_bytes)
    assert dom2 == b"veramem.timeline.signed_commitment.bundle.v1"

    signed_fields = {t.tag: t.value for t in tlvs2}

    version = signed_fields[1]
    assert version == b"\x01"

    message_to_sign = signed_fields[2]
    commit_algo = signed_fields[3].decode("ascii")
    commit_signature = signed_fields[4].decode("ascii")

    # =====================================================
    # Step 3 — Verify commitment signature
    # =====================================================
    signer.verify(
        message_to_sign,
        Signature(algo=commit_algo, value=commit_signature),
    )

    # =====================================================
    # Step 4 — Verify commitment integrity
    #
    # IMPORTANT:
    # The commitment is SHA-256 over the canonical message
    # encoded with domain:
    #     veramem.timeline.commitment.v1
    # =====================================================
    dom3, tlvs3 = decode_message(message_to_sign)
    assert dom3 == b"veramem.timeline.signed_commitment.v1"

    tags = {t.tag: t.value for t in tlvs3}

    head_b = tags[1]
    total_b = tags[2]
    ts_b = tags[3]
    commit_hex = tags[4].decode("ascii")

    # rebuild canonical commitment message
    commitment_msg = (
        b"VCE1"
        + (len(b"veramem.timeline.commitment.v1")).to_bytes(2, "big")
        + b"veramem.timeline.commitment.v1"
        + (1).to_bytes(2, "big") + len(head_b).to_bytes(4, "big") + head_b
        + (2).to_bytes(2, "big") + len(total_b).to_bytes(4, "big") + total_b
        + (3).to_bytes(2, "big") + len(ts_b).to_bytes(4, "big") + ts_b
    )

    recomputed_commit = sha256(commitment_msg).hexdigest()
    assert commit_hex == recomputed_commit

    # =====================================================
    # Step 5 — Verify attestation signature
    #
    # IMPORTANT:
    # The attestation signs:
    # - commitment signature metadata
    # - challenge hash
    #
    # Domain:
    #     veramem.device.attestation.v1
    # =====================================================
    att_payload = (
        b"VCE1"
        + (len(b"veramem.device.attestation.v1")).to_bytes(2, "big")
        + b"veramem.device.attestation.v1"
        + (1).to_bytes(2, "big")
        + len(commit_algo.encode("ascii")).to_bytes(4, "big")
        + commit_algo.encode("ascii")
        + (2).to_bytes(2, "big")
        + len(commit_signature.encode("ascii")).to_bytes(4, "big")
        + commit_signature.encode("ascii")
        + (3).to_bytes(2, "big")
        + len(challenge_hash).to_bytes(4, "big")
        + challenge_hash
    )

    signer.verify(
        att_payload,
        Signature(algo=att_algo, value=att_signature),
    )

    # =====================================================
    # Step 6 — Verify challenge
    # =====================================================
    expected_ch = sha256(challenge).digest()
    assert expected_ch == challenge_hash


def test_device_attestation_interop_tamper():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    commitment = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=commitment, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = bytearray(att.to_bytes())

    # flip a bit somewhere
    raw[-5] ^= 0x01

    dom, tlvs = decode_message(bytes(raw))
    fields = {t.tag: t.value for t in tlvs}

    signed_bytes = fields[1]
    challenge_hash = fields[2]
    att_algo = fields[3].decode("ascii")
    att_sig = fields[4].decode("ascii")

    # --- verify commitment signature ---
    dom2, tlvs2 = decode_message(signed_bytes)
    signed_fields = {t.tag: t.value for t in tlvs2}

    msg = signed_fields[1]
    commit_algo = signed_fields[2].decode("ascii")
    commit_sig = signed_fields[3].decode("ascii")

    commitment_failed = False
    try:
        signer.verify(msg, Signature(algo=commit_algo, value=commit_sig))
    except Exception:
        commitment_failed = True

    # --- verify attestation signature ---
    att_payload = (
        b"VCE1"
        + (len(b"veramem.device.attestation.v1")).to_bytes(2, "big")
        + b"veramem.device.attestation.v1"
        + (1).to_bytes(2, "big") + len(commit_algo.encode()).to_bytes(4, "big") + commit_algo.encode()
        + (2).to_bytes(2, "big") + len(commit_sig.encode()).to_bytes(4, "big") + commit_sig.encode()
        + (3).to_bytes(2, "big") + len(challenge_hash).to_bytes(4, "big") + challenge_hash
    )

    attestation_failed = False
    try:
        signer.verify(att_payload, Signature(algo=att_algo, value=att_sig))
    except Exception:
        attestation_failed = True

    # At least one layer must fail
    assert commitment_failed or attestation_failed
