# tests/test_domain_registry_kernel.py

import pytest

from veramem_kernel.common.domain_registry import DomainRegistry, Domain, DomainRegistryError


def test_domain_registry_rejects_collision():
    r = DomainRegistry()
    d = Domain(b"veramem.example.domain.v1")

    r.register(domain=d, owner="a")

    with pytest.raises(DomainRegistryError):
        r.register(domain=d, owner="b")


def test_domain_registry_accepts_distinct_domains():
    r = DomainRegistry()
    r.register(domain=Domain(b"veramem.a.v1"), owner="a")
    r.register(domain=Domain(b"veramem.b.v1"), owner="b")
