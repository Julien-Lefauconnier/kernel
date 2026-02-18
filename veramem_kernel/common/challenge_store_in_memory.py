# veramem_kernel/common/challenge_store_in_memory.py

from __future__ import annotations

from dataclasses import dataclass, field

from veramem_kernel.ports.challenge_store_port import (
    ChallengeStorePort,
    ChallengeRecord,
    ReplayError,
)


@dataclass
class InMemoryChallengeStore(ChallengeStorePort):
    _seen: set[str] = field(default_factory=set)

    def mark_used(self, record: ChallengeRecord) -> None:
        h = record.challenge_hash_hex
        if h in self._seen:
            raise ReplayError("challenge already used")
        self._seen.add(h)
