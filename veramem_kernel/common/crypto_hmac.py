# veramem_kernel/common/crypto_hmac.py

from __future__ import annotations

import hmac
from dataclasses import dataclass
from hashlib import sha256


class CryptoHmacError(ValueError):
    pass


def hmac_sha256_hex(*, key: bytes, message: bytes) -> str:
    if not isinstance(key, (bytes, bytearray)):
        raise CryptoHmacError("key must be bytes")
    return hmac.new(key, message, sha256).hexdigest()


def constant_time_eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)
