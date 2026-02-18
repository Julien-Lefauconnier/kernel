# tests/test_device_attestation_bytes_kernel.py

from datetime import datetime, timezone

import pytest

from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.journals.timeline.timeline_entry import (
    TimelineEntry,
    TimelineEntryNature,
)
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import (
    TimelineSignedCommitment,
)


def _entry(i: int) -> TimelineEntry:
    return TimelineEntry(
        entry_id=f"entry-{i:05d}",
        created_at=datetime.fromtimestamp(100 + i, tz=timezone.utc),
        type=TimelineEntryType.SYSTEM_NOTICE,
        title=f"t{i}",
        description=None,
        action_id=None,
        place_id=None,
        origin_ref="kernel",
        nature=TimelineEntryNature.EVENT,
    )


def test_device_attestation_bytes_roundtrip():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att1 = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = att1.to_bytes()
    att2 = DeviceAttestation.from_bytes(raw)

    # verify correctness after deserialize
    att2.verify(signer=signer, challenge=challenge)

    assert att1.challenge_hash_hex == att2.challenge_hash_hex
    assert att1.response == att2.response


def test_device_attestation_bytes_detects_corruption():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = bytearray(att.to_bytes())
    raw[-1] ^= 0x01  # bit flip

    corrupted = DeviceAttestation.from_bytes(bytes(raw))

    with pytest.raises(Exception):
        corrupted.verify(signer=signer, challenge=challenge)


def test_device_attestation_bytes_empty_snapshot():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"challenge"

    snap = TimelineSnapshot.build([])
    c = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    raw = att.to_bytes()
    att2 = DeviceAttestation.from_bytes(raw)

    att2.verify(signer=signer, challenge=challenge)
