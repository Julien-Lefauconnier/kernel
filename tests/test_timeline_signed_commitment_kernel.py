# tests/test_timeline_signed_commitment_kernel.py

import pytest
from datetime import datetime, timezone

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry, TimelineEntryNature
from veramem_kernel.journals.timeline.timeline_snapshot import TimelineSnapshot
from veramem_kernel.journals.timeline.timeline_types import TimelineEntryType
from veramem_kernel.journals.timeline.timeline_commitment import TimelineCommitment
from veramem_kernel.journals.timeline.timeline_signed_commitment import TimelineSignedCommitment
from veramem_kernel.ports.signer_port import SignerError


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


def test_signed_commitment_roundtrip():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)
    signed.verify(signer=signer)


def test_signed_commitment_rejects_wrong_signer():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))
    wrong = HmacSigner(key=b"another-secret!!".ljust(32, b"?"))

    snap = TimelineSnapshot.build([_entry(i) for i in range(5)])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)

    with pytest.raises(SignerError):
        signed.verify(signer=wrong)


def test_signed_commitment_empty_snapshot():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))

    snap = TimelineSnapshot.build([])
    c = TimelineCommitment.from_snapshot(snap)

    signed = TimelineSignedCommitment.sign(commitment=c, signer=signer)
    signed.verify(signer=signer)
