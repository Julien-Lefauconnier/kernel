# veramem_kernel/api/attestation.py
"""
Device attestation public API.

Stable abstraction over attestation formats.
"""

from ..common.device_attestation import DeviceAttestation
from ..common.challenge_store_in_memory import InMemoryChallengeStore

__all__ = [
    "DeviceAttestation",
    "InMemoryChallengeStore",
]
