# tests/test_public_api_surface.py

from __future__ import annotations

import pkgutil
import veramem_kernel.api as api


EXPECTED_SUBMODULES = [
    "attestation",
    "crypto",
    "encoding",
    "ports",
    "registry",
    "signals",
    "timeline",
]


def test_public_api_submodules_are_stable() -> None:
    found = sorted([m.name for m in pkgutil.iter_modules(api.__path__)])
    assert found == EXPECTED_SUBMODULES


def test_public_api___all___is_stable() -> None:
    assert getattr(api, "__all__", None) == [
        "timeline",
        "signals",
        "ports",
        "crypto",
        "attestation",
        "registry",
        "encoding",
    ]
