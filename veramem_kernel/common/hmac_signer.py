# veramem_kernel/common/hmac_signer.py

from __future__ import annotations

from dataclasses import dataclass

from veramem_kernel.common.crypto_hmac import hmac_sha256_hex, constant_time_eq
from veramem_kernel.ports.signer_port import Signature, SignerError

_HMAC_SHA256_HEX_LEN = 64

@dataclass(frozen=True)
class HmacSigner:
    """
    HMAC-SHA256 signer.

    Suitable for:
    - device-local secrets
    - hardware wallet symmetric attestation
    """

    key: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.key, (bytes, bytearray)):
             raise TypeError("HmacSigner key must be bytes")
        # Standard-level minimum: 256-bit key.
        # Refuse weak keys rather than warning: standards MUST be safe-by-default.
        if len(self.key) < 32:
            raise ValueError("HmacSigner key too short (min 32 bytes / 256-bit required)")

    def algorithm(self) -> str:
        return "hmac-sha256"

    def sign(self, message: bytes) -> Signature:
        sig = hmac_sha256_hex(key=self.key, message=message)
        return Signature(algo=self.algorithm(), value=sig)

    def verify(self, message: bytes, signature: Signature) -> None:
        if signature.algo != self.algorithm():
            raise SignerError("signature algorithm mismatch")
        
        # --- strict length enforcement (anti-truncation) ---
        if len(signature.value) != _HMAC_SHA256_HEX_LEN:
            raise SignerError("invalid signature length")

        expected = hmac_sha256_hex(key=self.key, message=message)
        if not constant_time_eq(expected, signature.value):
            raise SignerError("invalid signature")
