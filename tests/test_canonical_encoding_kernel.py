# tests/test_canonical_encoding_kernel.py

import pytest

from veramem_kernel.common.canonical_encoding import (
    TLV,
    encode_message,
    decode_message,
    CanonicalEncodingError,
    u64_be,
    ascii_bytes,
)


def test_tlv_roundtrip_decode():
    msg = encode_message(
        domain=b"veramem.test.domain",
        fields=(
            TLV(1, b"abc"),
            TLV(2, u64_be(42)),
            TLV(3, ascii_bytes("hello")),
        ),
    )

    domain, fields = decode_message(msg)
    assert domain == b"veramem.test.domain"
    assert fields[0].tag == 1 and fields[0].value == b"abc"
    assert fields[1].tag == 2 and fields[1].value == u64_be(42)
    assert fields[2].tag == 3 and fields[2].value == b"hello"


def test_tlv_is_deterministic():
    m1 = encode_message(
        domain=b"veramem.test",
        fields=(TLV(1, b"a"), TLV(2, b"b")),
    )
    m2 = encode_message(
        domain=b"veramem.test",
        fields=(TLV(1, b"a"), TLV(2, b"b")),
    )
    assert m1 == m2


def test_tlv_rejects_non_canonical_order():
    with pytest.raises(CanonicalEncodingError):
        encode_message(
            domain=b"veramem.test",
            fields=(TLV(2, b"b"), TLV(1, b"a")),
        )


def test_tlv_rejects_duplicate_tags():
    with pytest.raises(CanonicalEncodingError):
        encode_message(
            domain=b"veramem.test",
            fields=(TLV(1, b"a"), TLV(1, b"b")),
        )


def test_ascii_bytes_rejects_non_ascii():
    with pytest.raises(CanonicalEncodingError):
        ascii_bytes("€")


def test_u64_rejects_negative():
    with pytest.raises(CanonicalEncodingError):
        u64_be(-1)

def test_decode_rejects_bad_magic():
    with pytest.raises(CanonicalEncodingError):
        decode_message(b"NOPE" + b"\x00\x01a")

def test_decode_rejects_empty_domain():
    # MAGIC + domain_len=0
    with pytest.raises(CanonicalEncodingError):
        decode_message(b"VCE1" + b"\x00\x00")

def test_decode_rejects_truncated_domain():
    # domain_len=3 but only 2 bytes provided
    with pytest.raises(CanonicalEncodingError):
        decode_message(b"VCE1" + b"\x00\x03" + b"ab")

def test_decode_rejects_truncated_tlv_header():
    # valid domain, then only 5 bytes of TLV header (needs 6)
    msg = b"VCE1" + b"\x00\x01" + b"d" + b"\x00\x01\x00\x00\x00"
    with pytest.raises(CanonicalEncodingError):
        decode_message(msg)

def test_decode_rejects_truncated_tlv_value():
    # TAG=1 LEN=4 but only 3 bytes value
    msg = b"VCE1" + b"\x00\x01" + b"d" + b"\x00\x01" + b"\x00\x00\x00\x04" + b"abc"
    with pytest.raises(CanonicalEncodingError):
        decode_message(msg)

def test_decode_rejects_tag_zero():
    # TAG=0 is forbidden
    msg = b"VCE1" + b"\x00\x01" + b"d" + b"\x00\x00" + b"\x00\x00\x00\x01" + b"x"
    with pytest.raises(CanonicalEncodingError):
        decode_message(msg)
