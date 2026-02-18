# tests/test_device_attestation_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.common.device_attestation import DeviceAttestation


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


def test_device_attestation_roundtrip():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"random-challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    att.verify(signer=signer, challenge=challenge)


def test_device_attestation_rejects_wrong_challenge():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"random-challenge-123"
    wrong = b"another-challenge"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    with pytest.raises(ValueError):
        att.verify(signer=signer, challenge=wrong)


def test_device_attestation_rejects_wrong_signer():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    wrong = HmacSigner(key=b"another-secret!!".ljust(32, b"?"))
    challenge = b"random-challenge-123"

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    with pytest.raises(Exception):
        att.verify(signer=wrong, challenge=challenge)


def test_device_attestation_empty_snapshot():
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

    att.verify(signer=signer, challenge=challenge)
