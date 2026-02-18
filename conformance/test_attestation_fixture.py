# conformance/test_attestation_fixture.py


from pathlib import Path

from veramem_kernel.common.device_attestation import DeviceAttestation
from veramem_kernel.common.hmac_signer import HmacSigner


def test_attestation_fixture():
    raw = Path("conformance/fixtures/attestation_v1.bin").read_bytes()

    signer = HmacSigner(key=b"veramem-conformance-key".ljust(32, b"!"))

    challenge = b"conformance-challenge"

    att = DeviceAttestation.from_bytes(raw)
    att.verify(signer=signer, challenge=challenge)
