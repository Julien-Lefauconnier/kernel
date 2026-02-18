# veramem_kernel/common/tlv_schema.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Tuple

from veramem_kernel.common.canonical_encoding import (
    TLV,
    decode_message,
    encode_message,
    CanonicalEncodingError,
)


class TlvSchemaError(ValueError):
    pass


def _ascii_str(b: bytes) -> str:
    if not isinstance(b, (bytes, bytearray)):
        raise TlvSchemaError("expected bytes")
    try:
        s = bytes(b).decode("ascii")
    except Exception as e:
        raise TlvSchemaError("expected ASCII bytes") from e
    # forbid control chars for auditability (same spirit as ascii_bytes)
    if any(ord(c) < 32 for c in s):
        raise TlvSchemaError("ASCII contains control characters")
    return s


def _u64_from_be(b: bytes) -> int:
    if not isinstance(b, (bytes, bytearray)) or len(b) != 8:
        raise TlvSchemaError("expected u64 (8 bytes)")
    return int.from_bytes(b, "big", signed=False)


@dataclass(frozen=True)
class MessageSchema:
    domain: bytes
    required_tags: Tuple[int, ...]
    allow_empty: Tuple[int, ...] = ()
    reject_unknown: bool = True

    def parse(self, msg: bytes) -> Dict[int, bytes]:
        try:
            dom, tlvs = decode_message(msg)
        except CanonicalEncodingError as e:
            raise TlvSchemaError(str(e)) from e

        if dom != self.domain:
            raise TlvSchemaError("domain mismatch")

        m: Dict[int, bytes] = {}
        for t in tlvs:
            m[t.tag] = bytes(t.value)

        for tag in self.required_tags:
            if tag not in m:
                raise TlvSchemaError(f"missing required tag {tag}")
            if len(m[tag]) == 0 and tag not in self.allow_empty:
                raise TlvSchemaError(f"tag {tag} must not be empty")

        if self.reject_unknown:
            allowed = set(self.required_tags)
            for tag in m.keys():
                if tag not in allowed:
                    raise TlvSchemaError(f"unknown tag {tag}")

        return m


def build_message(*, domain, fields: Iterable[TLV]) -> bytes:
    """
    Unified canonical message builder.

    Accepts:
    - raw bytes domains
    - Domain registry handles (with .name attribute)
    """

    if isinstance(domain, (bytes, bytearray)):
        dom = bytes(domain)
    else:
        # Registry Domain handle
        try:
            dom = domain.name
        except AttributeError as e:
            raise TlvSchemaError("invalid domain type") from e

    return encode_message(domain=dom, fields=fields)



def as_ascii(m: Mapping[int, bytes], tag: int) -> str:
    return _ascii_str(m[tag])


def as_u64(m: Mapping[int, bytes], tag: int) -> int:
    return _u64_from_be(m[tag])


def as_bytes(m: Mapping[int, bytes], tag: int, *, ln: int | None = None) -> bytes:
    b = bytes(m[tag])
    if ln is not None and len(b) != ln:
        raise TlvSchemaError(f"tag {tag} wrong length")
    return b
