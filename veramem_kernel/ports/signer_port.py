# veramem_kernel/ports/signer_port.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class SignerError(ValueError):
    pass


@dataclass(frozen=True)
class Signature:
    """
    Versioned signature container.

    algo: identifies the algorithm (e.g., "hmac-sha256", "ed25519")
    value: hex/base64 signature payload (we keep hex for now)
    """

    algo: str
    value: str

    def __post_init__(self) -> None:
        if not self.algo or not isinstance(self.algo, str):
            raise SignerError("Signature.algo must be a non-empty string")
        if not self.value or not isinstance(self.value, str):
            raise SignerError("Signature.value must be a non-empty string")
        if len(self.algo) > 32:
            raise SignerError("Signature.algo too long")

        if not self.algo.isascii():
            raise SignerError("Signature.algo must be ASCII")

        if any(c.isspace() for c in self.algo):
            raise SignerError("Signature.algo must not contain whitespace")

        if any(ord(c) < 33 or ord(c) > 126 for c in self.algo):
            raise SignerError("Signature.algo must be printable ASCII")

        if not self.value or not isinstance(self.value, str):
            raise SignerError("Signature.value must be a non-empty string")

        if not self.value.isascii():
            raise SignerError("Signature.value must be ASCII")

        if len(self.value) < 32:
            raise SignerError("Signature.value too short")

        if len(self.value) % 2 != 0:
            raise SignerError("Signature.value must have even length")

        if any(c not in "0123456789abcdef" for c in self.value):
            raise SignerError("Signature.value must be lowercase hex")


class SignerPort(Protocol):
    """
    Kernel port for signing and verifying messages.

    This decouples the kernel from any specific crypto backend.
    """

    def algorithm(self) -> str:
        ...

    def sign(self, message: bytes) -> Signature:
        ...

    def verify(self, message: bytes, signature: Signature) -> None:
        ...
