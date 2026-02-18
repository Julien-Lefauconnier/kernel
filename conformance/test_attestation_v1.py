# conformance/test_attestation_v1.py

from hashlib import sha256

from veramem_kernel.common.canonical_encoding import decode_message
from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.ports.signer_port import Signature

from conformance.utils import build_entry


def test_attestation_v1_conformance():
    """
    Public conformance test for Veramem attestation protocol v1.
    This must pass for any compliant implementation.
    """

    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge-123"

    # === deterministic snapshot ===
    snap = TimelineSnapshot.build([build_entry(i) for i in range(5)])
    commitment = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=commitment, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = att.to_bytes()

    # === Step 1: parse attestation bundle ===
    dom, tlvs = decode_message(raw)
    assert dom == b"veramem.device.attestation.bundle.v1"

    fields = {t.tag: t.value for t in tlvs}

    signed_bytes = fields[1]
    challenge_hash = fields[2]
    att_algo = fields[3].decode("ascii")
    att_signature = fields[4].decode("ascii")

    # === Step 2: parse signed commitment bundle ===
    dom2, tlvs2 = decode_message(signed_bytes)
    assert dom2 == b"veramem.timeline.signed_commitment.bundle.v1"

    signed_fields = {t.tag: t.value for t in tlvs2}

    message_to_sign = signed_fields[2]
    commit_algo = signed_fields[3].decode("ascii")
    commit_signature = signed_fields[4].decode("ascii")

    # === Step 3: verify commitment signature ===
    signer.verify(
        message_to_sign,
        Signature(algo=commit_algo, value=commit_signature),
    )

    # === Step 4: verify timeline commitment ===
    dom3, tlvs3 = decode_message(message_to_sign)
    assert dom3 == b"veramem.timeline.signed_commitment.v1"

    tags = {t.tag: t.value for t in tlvs3}

    head_b = tags[1]
    total_b = tags[2]
    ts_b = tags[3]
    commit_hex = tags[4].decode("ascii")

    commitment_msg = (
        b"VCE1"
        + (len(b"veramem.timeline.commitment.v1")).to_bytes(2, "big")
        + b"veramem.timeline.commitment.v1"
        + (1).to_bytes(2, "big") + len(head_b).to_bytes(4, "big") + head_b
        + (2).to_bytes(2, "big") + len(total_b).to_bytes(4, "big") + total_b
        + (3).to_bytes(2, "big") + len(ts_b).to_bytes(4, "big") + ts_b
    )

    recomputed = sha256(commitment_msg).hexdigest()
    assert commit_hex == recomputed

    # === Step 5: verify attestation signature ===
    att_payload = (
        b"VCE1"
        + (len(b"veramem.device.attestation.v1")).to_bytes(2, "big")
        + b"veramem.device.attestation.v1"
        + (1).to_bytes(2, "big") + len(commit_algo.encode("ascii")).to_bytes(4, "big") + commit_algo.encode("ascii")
        + (2).to_bytes(2, "big") + len(commit_signature.encode("ascii")).to_bytes(4, "big") + commit_signature.encode("ascii")
        + (3).to_bytes(2, "big") + len(challenge_hash).to_bytes(4, "big") + challenge_hash
    )

    signer.verify(
        att_payload,
        Signature(algo=att_algo, value=att_signature),
    )

    # === Step 6: verify challenge ===
    assert sha256(challenge).digest() == challenge_hash
