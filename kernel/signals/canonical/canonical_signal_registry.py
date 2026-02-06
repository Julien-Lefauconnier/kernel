# kernel/signals/canonical/canonical_signal_registry.py

from typing import Dict, Tuple
from .canonical_signal_key import CanonicalSignalKey
from .canonical_signal_spec import CanonicalSignalSpec


class CanonicalSignalRegistry:
    _registry: Dict[CanonicalSignalKey, CanonicalSignalSpec] = {}

    @classmethod
    def register(cls, spec: CanonicalSignalSpec) -> None:
        if spec.key in cls._registry:
            raise ValueError(f"Duplicate CanonicalSignalKey: {spec.key}")
        cls._registry[spec.key] = spec

    @classmethod
    def get(cls, key: CanonicalSignalKey) -> CanonicalSignalSpec:
        try:
            return cls._registry[key]
        except KeyError:
            raise KeyError(f"CanonicalSignalKey not registered: {key}")

    @classmethod
    def has(cls, key: CanonicalSignalKey) -> bool:
        return key in cls._registry

    @classmethod
    def all(cls) -> Tuple[CanonicalSignalSpec, ...]:
        return tuple(cls._registry.values())
