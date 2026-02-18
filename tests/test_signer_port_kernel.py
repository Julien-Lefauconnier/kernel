# tests/test_signer_port_kernel.py

import pytest

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.ports.signer_port import Signature, SignerError


def test_signature_invariants():
    Signature(algo="hmac-sha256", value="a" * 64)
    with pytest.raises(SignerError):
        Signature(algo="", value="x")
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256", value="")


def test_hmac_signer_roundtrip():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))

    msg = b"hello"
    sig = signer.sign(msg)

    assert sig.algo == "hmac-sha256"
    signer.verify(msg, sig)


def test_hmac_signer_rejects_wrong_message():
    signer = HmacSigner(key=b"test-device-secret".ljust(32, b"!"))

    sig = signer.sign(b"hello")

    with pytest.raises(SignerError):
        signer.verify(b"HELLO", sig)
