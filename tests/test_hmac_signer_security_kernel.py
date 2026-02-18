# tests/test_hmac_signer_security_kernel.py

import pytest

from veramem_kernel.common.hmac_signer import HmacSigner
from veramem_kernel.ports.signer_port import Signature, SignerError


def test_hmac_rejects_truncated_signature():
    signer = HmacSigner(key=b"secret-12345678".ljust(32, b"#"))
    msg = b"hello"

    sig = signer.sign(msg)

    truncated = Signature(algo=sig.algo, value=sig.value[:-2])

    with pytest.raises(SignerError):
        signer.verify(msg, truncated)


def test_hmac_rejects_extended_signature():
    signer = HmacSigner(key=b"secret-12345678".ljust(32, b"#"))
    msg = b"hello"

    sig = signer.sign(msg)

    extended = Signature(algo=sig.algo, value=sig.value + "00")

    with pytest.raises(SignerError):
        signer.verify(msg, extended)


def test_hmac_rejects_algo_confusion():
    signer = HmacSigner(key=b"secret-12345678".ljust(32, b"#"))
    msg = b"hello"

    sig = signer.sign(msg)

    bad = Signature(algo="ed25519", value=sig.value)

    with pytest.raises(SignerError):
        signer.verify(msg, bad)
