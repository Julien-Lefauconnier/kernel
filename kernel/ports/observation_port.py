# kernel/ports/observation_port.py

from __future__ import annotations

from typing import Iterable, Protocol

from kernel.journals.observation.observation_event import ObservationEvent
from kernel.journals.observation.patterns.normative_pattern import NormativePattern


class ObservationWriterPort(Protocol):
    """
    Kernel port: append-only writer for observation events.
    """

    def record(self, event: ObservationEvent) -> None: ...


class NormativePatternProviderPort(Protocol):
    """
    Kernel port: read-only provider for normative patterns.
    Used by governance explainability wiring (stack reads patterns, kernel defines contract).
    """

    def list_patterns(self, *, user_id: str) -> Iterable[NormativePattern]: ...


# Legacy name (to be removed in v0.2)
ObservationPort = ObservationWriterPort
