# kernel/signals/canonical/canonical_signal_registry.py

from typing import Dict, Tuple
from threading import Lock
from .canonical_signal_key import CanonicalSignalKey
from .canonical_signal_spec import CanonicalSignalSpec


class CanonicalSignalRegistry:
    _registry: Dict[CanonicalSignalKey, CanonicalSignalSpec] = {}
    _frozen: bool = False
    _lock = Lock()

    @classmethod
    def register(cls, spec: CanonicalSignalSpec) -> None:
        with cls._lock:
            if cls._frozen:
                raise RuntimeError("CanonicalSignalRegistry is frozen")

            if spec.key in cls._registry:
                raise ValueError(f"Duplicate CanonicalSignalKey: {spec.key}")
            cls._registry[spec.key] = spec

    @classmethod
    def get(cls, key: CanonicalSignalKey) -> CanonicalSignalSpec:
        with cls._lock:
            try:
                return cls._registry[key]
            except KeyError:
                raise KeyError(f"CanonicalSignalKey not registered: {key}")

    @classmethod
    def has(cls, key: CanonicalSignalKey) -> bool:
        with cls._lock:
            return key in cls._registry

    @classmethod
    def all(cls) -> Tuple[CanonicalSignalSpec, ...]:
        with cls._lock:
            return tuple(cls._registry.values())
    
    @classmethod
    def _clear_for_tests(cls) -> None:
        with cls._lock:
            cls._registry.clear()
            cls._frozen = False

    @classmethod
    def freeze(cls) -> None:
        with cls._lock:
            cls._frozen = True


def register_all_canonical_signals() -> None:
    """
    Bootstrap complet du registry canonique.
    Appelée automatiquement au premier import du module canonical.
    """
    from .specs.timeline import register_timeline_signals
    from .specs.memory_long import register_memory_long_signals
    from .specs.decision import register_decision_signals
    from .specs.risk import register_risk_signals
    from .specs.validation import register_validation_signals

    register_timeline_signals()
    register_memory_long_signals()
    register_decision_signals()
    register_risk_signals()
    register_validation_signals()