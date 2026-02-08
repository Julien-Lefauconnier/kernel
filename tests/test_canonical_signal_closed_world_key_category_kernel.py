# tests/test_canonical_signal_closed_world_key_category_kernel.py

import pytest
from kernel.signals.canonical import (
    CanonicalSignalKey,
    CanonicalSignalCategory,
)
from kernel.signals.canonical.canonical_signal_registry import (
    CanonicalSignalRegistry,
)


def test_same_code_different_category_is_rejected():
    CanonicalSignalRegistry._clear_for_tests()

    # Le closed world est porté par l'Enum lui-même :
    # une catégorie non prévue est inconstructible.
    with pytest.raises(AttributeError):
        CanonicalSignalKey(
            category=CanonicalSignalCategory.OBSERVATION,  # catégorie inexistante
            code="memory_long_projected",
        )
