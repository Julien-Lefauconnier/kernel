# tests/test_signal_lineage_patch_kernel.py

from dataclasses import FrozenInstanceError

import pytest

from veramem_kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from veramem_kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from veramem_kernel.signals.lineage.signal_lineage_patch import (
    SignalLineagePatch,
    SignalLineagePatchType,
)


def _key(code: str) -> CanonicalSignalKey:
    return CanonicalSignalKey(
        CanonicalSignalCategory.OBSERVATION_STATE,
        code,
    )


# ---------------------------------------------------------------------------
# Patch type enum
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_type_enum_is_strict():
    assert SignalLineagePatchType.ADD.name == "ADD"
    assert SignalLineagePatchType.REMOVE.name == "REMOVE"
    assert SignalLineagePatchType.MOVE.name == "MOVE"
    assert SignalLineagePatchType.REWIRE_PARENTS.name == "REWIRE_PARENTS"


# ---------------------------------------------------------------------------
# Patch immutability
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_is_immutable():
    patch = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("A"),
        parents=(),
    )

    with pytest.raises(FrozenInstanceError):
        patch.key = _key("B")


# ---------------------------------------------------------------------------
# ADD patch
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_add_is_valid():
    patch = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("A"),
        parents=(),
    )

    assert patch.type is SignalLineagePatchType.ADD
    assert patch.key.code == "A"
    assert patch.parents == ()


# ---------------------------------------------------------------------------
# REMOVE patch
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_remove_has_no_parents():
    patch = SignalLineagePatch(
        type=SignalLineagePatchType.REMOVE,
        key=_key("A"),
        parents=None,
    )

    assert patch.type is SignalLineagePatchType.REMOVE
    assert patch.parents is None


# ---------------------------------------------------------------------------
# MOVE patch
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_move_has_no_parents_payload():
    patch = SignalLineagePatch(
        type=SignalLineagePatchType.MOVE,
        key=_key("A"),
        parents=None,
    )

    assert patch.type is SignalLineagePatchType.MOVE
    assert patch.parents is None


# ---------------------------------------------------------------------------
# REWIRE_PARENTS patch
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_rewire_parents_contains_new_parents():
    A = _key("A")
    B = _key("B")
    C = _key("C")

    patch = SignalLineagePatch(
        type=SignalLineagePatchType.REWIRE_PARENTS,
        key=C,
        parents=(A, B),
    )

    assert patch.type is SignalLineagePatchType.REWIRE_PARENTS
    assert patch.parents == (A, B)


# ---------------------------------------------------------------------------
# Equality & determinism
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_equality_is_structural():
    p1 = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("A"),
        parents=(),
    )

    p2 = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("A"),
        parents=(),
    )

    assert p1 == p2


def test_signal_lineage_patch_inequality_on_payload():
    p1 = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("A"),
        parents=(),
    )

    p2 = SignalLineagePatch(
        type=SignalLineagePatchType.ADD,
        key=_key("B"),
        parents=(),
    )

    assert p1 != p2


# ---------------------------------------------------------------------------
# Defensive semantics
# ---------------------------------------------------------------------------

def test_signal_lineage_patch_repr_is_stable():
    patch = SignalLineagePatch(
        type=SignalLineagePatchType.REMOVE,
        key=_key("A"),
        parents=None,
    )

    r = repr(patch)

    assert "SignalLineagePatch" in r
    assert "REMOVE" in r
    assert "A" in r
