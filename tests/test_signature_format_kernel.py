# tests/test_signature_format_kernel.py

import pytest

from veramem_kernel.ports.signer_port import Signature, SignerError


def test_signature_accepts_valid_hex():
    s = Signature(algo="hmac-sha256", value="a" * 64)
    assert s.algo == "hmac-sha256"
    assert s.value == "a" * 64


def test_signature_rejects_uppercase_hex():
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256", value="A" * 64)


def test_signature_rejects_non_hex():
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256", value="g" * 64)  # g not hex


def test_signature_rejects_odd_length():
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256", value="a" * 63)


def test_signature_rejects_too_short():
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256", value="a" * 10)


def test_signature_rejects_algo_with_space():
    with pytest.raises(SignerError):
        Signature(algo="hmac sha256", value="a" * 64)


def test_signature_rejects_algo_non_ascii():
    with pytest.raises(SignerError):
        Signature(algo="hmac-sha256-€", value="a" * 64)


def test_signature_rejects_algo_too_long():
    with pytest.raises(SignerError):
        Signature(algo="x" * 33, value="a" * 64)
