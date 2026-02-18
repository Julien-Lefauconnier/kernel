# tests/test_canonical_signal_closed_world_kernel.py

import pytest

from veramem_kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalCategory,
    CanonicalSignalKey,
)
from veramem_kernel.invariants.signal.canonical.canonical_signal_invariants import (
    validate_canonical_signal,
)
from veramem_kernel.signals.canonical.canonical_signal_registry import CanonicalSignalRegistry



def test_unregistered_canonical_signal_key_is_rejected():
    CanonicalSignalRegistry._clear_for_tests()

    with pytest.raises(KeyError):
        CanonicalSignal(
            signal_id="sig-x",
            key=CanonicalSignalKey(
                CanonicalSignalCategory.COGNITIVE_STATE,
                "non_existing_signal",
            ),
            state="ANY",
            subject_ref="x",
            temporal_anchor="t-x",
            origin="journal",
            supersedes=None,
        )

