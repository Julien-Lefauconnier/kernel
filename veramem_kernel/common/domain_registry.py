# veramem_kernel/common/domain_registry.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


class DomainRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class Domain:
    """
    Canonical domain identifier for kernel message formats.

    Rules:
    - bytes
    - ASCII only
    - non-empty
    - no whitespace
    """
    value: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.value, (bytes, bytearray)) or len(self.value) == 0:
            raise DomainRegistryError("Domain must be non-empty bytes")

        try:
            s = self.value.decode("ascii")
        except Exception as e:
            raise DomainRegistryError("Domain must be ASCII") from e

        if any(c.isspace() for c in s):
            raise DomainRegistryError("Domain must not contain whitespace")


class DomainRegistry:
    """
    Global registry for all kernel domains.
    Prevents collisions and makes audit/versioning explicit.
    """

    def __init__(self) -> None:
        self._domains: Dict[bytes, str] = {}

    def register(self, *, domain: Domain, owner: str) -> bytes:
        if domain.value in self._domains:
            prev = self._domains[domain.value]
            raise DomainRegistryError(
                f"Domain collision: {domain.value!r} already registered by {prev}, attempted by {owner}"
            )
        self._domains[domain.value] = owner
        return domain.value

    def list(self) -> Dict[bytes, str]:
        return dict(self._domains)


# Global singleton registry (import-time registration)
REGISTRY = DomainRegistry()
