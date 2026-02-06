# tests/test_canonical_signal_closed_world_kernel.py

import pytest

from kernel.signals.canonical import (
    CanonicalSignal,
    CanonicalSignalCategory,
    CanonicalSignalKey,
)
from kernel.invariants.signal.canonical.canonical_signal_invariants import (
    validate_canonical_signal,
)



def test_unregistered_canonical_signal_key_is_rejected():
    signal = CanonicalSignal(
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

    with pytest.raises(KeyError):
        validate_canonical_signal(signal)
