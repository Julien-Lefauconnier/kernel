# veramem_kernel/common/canonical_encoding.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

_MAGIC = b"VCE1"  # Veramem Canonical Encoding v1


class CanonicalEncodingError(ValueError):
    pass


@dataclass(frozen=True)
class TLV:
    tag: int
    value: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.tag, int) or self.tag <= 0 or self.tag > 0xFFFF:
            raise CanonicalEncodingError("TLV.tag must be int in [1..65535]")
        if not isinstance(self.value, (bytes, bytearray)):
            raise CanonicalEncodingError("TLV.value must be bytes")


def u64_be(n: int) -> bytes:
    if not isinstance(n, int) or n < 0 or n > 0xFFFFFFFFFFFFFFFF:
        raise CanonicalEncodingError("u64 out of range")
    return n.to_bytes(8, "big", signed=False)


def ascii_bytes(s: str) -> bytes:
    if not isinstance(s, str):
        raise CanonicalEncodingError("ascii_bytes expects str")
    if not s.isascii():
        raise CanonicalEncodingError("string must be ASCII")
    # forbid NUL and control chars for safety/auditability
    if any(ord(c) < 32 for c in s):
        raise CanonicalEncodingError("string contains control characters")
    return s.encode("ascii")


def encode_message(*, domain: bytes, fields: Iterable[TLV]) -> bytes:
    """
    Canonical message format (VCE1):

        MAGIC(4) ||
        DOMAIN_LEN(u16) || DOMAIN(bytes) ||
        TLV... where each TLV is:
            TAG(u16) || LEN(u32) || VALUE(bytes)

    Canonicalization rules:
    - tags must be strictly increasing
    - no duplicates
    - domain must be non-empty bytes (ASCII recommended)
    """

    if not isinstance(domain, (bytes, bytearray)) or len(domain) == 0:
        raise CanonicalEncodingError("domain must be non-empty bytes")
    if len(domain) > 0xFFFF:
        raise CanonicalEncodingError("domain too long")

    items = tuple(fields)
    # enforce canonical ordering + uniqueness
    last_tag = 0
    for f in items:
        if not isinstance(f, TLV):
            raise CanonicalEncodingError("fields must be TLV instances")
        if f.tag <= last_tag:
            raise CanonicalEncodingError("TLV tags must be strictly increasing")
        last_tag = f.tag
        if len(f.value) > 0xFFFFFFFF:
            raise CanonicalEncodingError("TLV value too large")

    out = bytearray()
    out += _MAGIC
    out += int(len(domain)).to_bytes(2, "big", signed=False)
    out += bytes(domain)

    for f in items:
        out += int(f.tag).to_bytes(2, "big", signed=False)
        out += int(len(f.value)).to_bytes(4, "big", signed=False)
        out += bytes(f.value)

    return bytes(out)


def decode_message(msg: bytes) -> Tuple[bytes, Tuple[TLV, ...]]:
    """
    Strict decoder, mostly for tests/audits.

    Returns: (domain, tlvs)
    """
    if not isinstance(msg, (bytes, bytearray)):
        raise CanonicalEncodingError("msg must be bytes")

    b = memoryview(msg)
    if len(b) < 6:
        raise CanonicalEncodingError("message too short")

    if bytes(b[:4]) != _MAGIC:
        raise CanonicalEncodingError("bad magic")

    pos = 4
    domain_len = int.from_bytes(b[pos : pos + 2], "big", signed=False)
    pos += 2
    if domain_len == 0:
        raise CanonicalEncodingError("empty domain")
    if len(b) < pos + domain_len:
        raise CanonicalEncodingError("truncated domain")
    domain = bytes(b[pos : pos + domain_len])
    pos += domain_len

    tlvs = []
    last_tag = 0
    while pos < len(b):
        if len(b) - pos < 6:
            raise CanonicalEncodingError("truncated TLV header")
        tag = int.from_bytes(b[pos : pos + 2], "big", signed=False)
        pos += 2
        ln = int.from_bytes(b[pos : pos + 4], "big", signed=False)
        pos += 4
        if len(b) - pos < ln:
            raise CanonicalEncodingError("truncated TLV value")
        val = bytes(b[pos : pos + ln])
        pos += ln

        if tag == 0:
            raise CanonicalEncodingError("invalid TLV tag (0)")
        if tag <= last_tag:
            raise CanonicalEncodingError("non-canonical TLV ordering")
        last_tag = tag

        tlvs.append(TLV(tag=tag, value=val))

    return domain, tuple(tlvs)
