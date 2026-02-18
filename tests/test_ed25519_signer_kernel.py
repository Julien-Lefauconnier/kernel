# tests/test_ed25519_signer_kernel.py


import os

from veramem_kernel.common.ed25519_signer import Ed25519Signer


def test_ed25519_roundtrip():
    seed = b"\x01" * 32
    signer = Ed25519Signer.from_seed(seed)

    msg = b"veramem-test"
    sig = signer.sign(msg)

    signer.verify(msg, sig)


def test_ed25519_deterministic():
    seed = b"\x02" * 32
    signer = Ed25519Signer.from_seed(seed)

    msg = b"determinism"
    s1 = signer.sign(msg)
    s2 = signer.sign(msg)

    assert s1.value == s2.value


def test_ed25519_detects_corruption():
    seed = b"\x03" * 32
    signer = Ed25519Signer.from_seed(seed)

    msg = b"secure"
    sig = signer.sign(msg)

    corrupted = sig.value[:-2] + "ff"

    from veramem_kernel.ports.signer_port import Signature, SignerError

    try:
        signer.verify(msg, Signature(algo="ed25519", value=corrupted))
        assert False
    except SignerError:
        pass


def test_ed25519_public_key_stable():
    seed = b"\x04" * 32
    s1 = Ed25519Signer.from_seed(seed)
    s2 = Ed25519Signer.from_seed(seed)

    assert s1.public_key_hex() == s2.public_key_hex()
