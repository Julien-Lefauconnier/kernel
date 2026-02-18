# veramem_kernel/ports/challenge_store_port.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ReplayError(ValueError):
    pass


@dataclass(frozen=True)
class ChallengeRecord:
    """
    Record stored by verifier to prevent replay.
    """
    challenge_hash_hex: str


class ChallengeStorePort(Protocol):
    """
    Verifier-side anti-replay storage.
    """

    def mark_used(self, record: ChallengeRecord) -> None:
        """
        Must raise ReplayError if record already exists.
        """
        ...
