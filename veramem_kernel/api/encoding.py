# veramem_kernel/api/encoding.py
"""
Canonical encoding public API.

Deterministic binary representation for:
- commitments
- signatures
- attestations
- interop
"""

from ..common.canonical_encoding import (
    u64_be,
    ascii_bytes,
    encode_message,
    decode_message,
)

from ..common.tlv_schema import (
    MessageSchema,
    TlvSchemaError,
)

__all__ = [
    "u64_be",
    "ascii_bytes",
    "encode_message",
    "decode_message",
    "MessageSchema",
    "TlvSchemaError",
]
