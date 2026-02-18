# veramem_kernel/common/ed25519_signer.py

from __future__ import annotations

from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

from veramem_kernel.ports.signer_port import Signature, SignerError


class Ed25519Signer:
    """
    Ed25519 signer compatible with Veramem SignerPort.

    Properties:
    - deterministic
    - constant-time verification
    - canonical hex encoding
    - domain-separated at message level
    """

    def __init__(self, signing_key: SigningKey):
        if not isinstance(signing_key, SigningKey):
            raise ValueError("invalid signing key")

        self._sk = signing_key
        self._vk: VerifyKey = signing_key.verify_key

    @classmethod
    def from_seed(cls, seed: bytes) -> "Ed25519Signer":
        """
        Deterministic constructor (useful for fixtures and tests).
        """
        if len(seed) != 32:
            raise ValueError("ed25519 seed must be 32 bytes")
        return cls(SigningKey(seed))

    def public_key_hex(self) -> str:
        return self._vk.encode().hex()

    def algorithm(self) -> str:
        return "ed25519"

    def sign(self, message: bytes) -> Signature:
        if not isinstance(message, (bytes, bytearray)):
            raise ValueError("message must be bytes")

        sig = self._sk.sign(message).signature.hex()
        return Signature(algo=self.algorithm(), value=sig)

    def verify(self, message: bytes, signature: Signature) -> None:
        if signature.algo != self.algorithm():
            raise SignerError("signature algorithm mismatch")

        try:
            raw = bytes.fromhex(signature.value)
        except ValueError:
            raise SignerError("invalid signature encoding")

        try:
            self._vk.verify(message, raw)
        except BadSignatureError:
            raise SignerError("invalid signature")
