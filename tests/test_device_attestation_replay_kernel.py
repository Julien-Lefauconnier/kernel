# tests/test_device_attestation_replay_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.common.challenge_store_in_memory import InMemoryChallengeStore
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.ports.challenge_store_port import ReplayError


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


def test_device_attestation_replay_is_rejected():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"random-challenge-123"
    store = InMemoryChallengeStore()

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    att.verify_with_store(signer=signer, challenge=challenge, store=store)

    with pytest.raises(ReplayError):
        att.verify_with_store(signer=signer, challenge=challenge, store=store)


def test_device_attestation_invalid_does_not_burn_challenge():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    challenge = b"random-challenge-123"
    store = InMemoryChallengeStore()

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)
    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    att = DeviceAttestation.respond(
        signed_commitment=signed,
        signer=signer,
        challenge=challenge,
    )

    # Wrong challenge => verification fails, should NOT be stored as used
    with pytest.raises(ValueError):
        att.verify_with_store(signer=signer, challenge=b"wrong", store=store)

    # Now the correct one should still be accepted
    att.verify_with_store(signer=signer, challenge=challenge, store=store)
