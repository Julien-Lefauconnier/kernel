# veramem_kernel/journals/timeline/timeline_hashchain.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Iterable, List

from veramem_kernel.journals.timeline.timeline_entry import TimelineEntry


def _dt_iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        raise ValueError("datetime must be tz-aware")
    off = dt.tzinfo.utcoffset(dt)
    if off is None or off.total_seconds() != 0:
        raise ValueError("datetime must be UTC")
    return dt.isoformat()


def _canonical_entry_payload(e: TimelineEntry) -> dict:
    # IMPORTANT: explicit list, stable order via json sort_keys=True
    return {
        "entry_id": e.entry_id,
        "created_at": _dt_iso_utc(e.created_at),
        "type": str(e.type.value) if hasattr(e.type, "value") else str(e.type),
        "title": e.title,
        "description": e.description,
        "action_id": e.action_id,
        "place_id": e.place_id,
        "origin_ref": e.origin_ref,
        "nature": str(e.nature.value) if hasattr(e.nature, "value") else str(e.nature),
        "device_id": e.device_id,
        "lamport": e.lamport,   
    }


def hash_entry(e: TimelineEntry) -> str:
    payload = _canonical_entry_payload(e)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(raw.encode("utf-8")).hexdigest()


def chain_hashes(entries: Iterable[TimelineEntry], *, seed: str = "") -> List[str]:
    prev = seed
    out: List[str] = []
    for e in entries:
        h_e = hash_entry(e)
        prev = sha256((prev + h_e).encode("utf-8")).hexdigest()
        out.append(prev)
    return out


@dataclass(frozen=True)
class TimelineHashChain:
    hashes: tuple[str, ...]

    @property
    def head(self) -> str | None:
        return self.hashes[-1] if self.hashes else None

    @classmethod
    def build(cls, entries: Iterable[TimelineEntry], *, seed: str = "") -> "TimelineHashChain":
        return cls(tuple(chain_hashes(entries, seed=seed)))

    def verify(self, entries: Iterable[TimelineEntry], *, seed: str = "") -> None:
        expected = tuple(chain_hashes(entries, seed=seed))
        if expected != self.hashes:
            raise ValueError("timeline hashchain verification failed")

    def append(self, entry: TimelineEntry, *, seed: str = "") -> "TimelineHashChain":
        """
        Deterministic incremental extension of the hashchain.

        Guarantees strict equivalence with batch build.
        """

        h_e = hash_entry(entry)

        prev = self.head or seed
        new_hash = sha256((prev + h_e).encode("utf-8")).hexdigest()

        return TimelineHashChain(self.hashes + (new_hash,))
