# tests/test_signal_lineage_patch_builder_kernel.py

from kernel.signals.canonical.canonical_signal_category import CanonicalSignalCategory
from kernel.signals.canonical.canonical_signal_key import CanonicalSignalKey
from kernel.signals.lineage.signal_lineage_patch import (
    SignalLineagePatch,
    SignalLineagePatchType,
)
from kernel.signals.lineage.signal_lineage_diff import SignalLineageDiff
from kernel.signals.lineage.signal_lineage_patch_builder import (
    build_signal_lineage_patches,
)


def test_patch_builder_returns_empty_for_empty_diff():
    diff = SignalLineageDiff(
        added=frozenset(),
        removed=frozenset(),
        moved=frozenset(),
        changed_parents=frozenset(),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == ()


def test_patch_builder_creates_add_patches():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    diff = SignalLineageDiff(
        added=frozenset({A}),
        removed=frozenset(),
        moved=frozenset(),
        changed_parents=frozenset(),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == (
        SignalLineagePatch(
            type=SignalLineagePatchType.ADD,
            signal=A,
        ),
    )


def test_patch_builder_creates_remove_patches():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    diff = SignalLineageDiff(
        added=frozenset(),
        removed=frozenset({A}),
        moved=frozenset(),
        changed_parents=frozenset(),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == (
        SignalLineagePatch(
            type=SignalLineagePatchType.REMOVE,
            signal=A,
        ),
    )


def test_patch_builder_creates_move_patches():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    diff = SignalLineageDiff(
        added=frozenset(),
        removed=frozenset(),
        moved=frozenset({A}),
        changed_parents=frozenset(),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == (
        SignalLineagePatch(
            type=SignalLineagePatchType.MOVE,
            signal=A,
        ),
    )


def test_patch_builder_creates_rewire_patches():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")

    diff = SignalLineageDiff(
        added=frozenset(),
        removed=frozenset(),
        moved=frozenset(),
        changed_parents=frozenset({A}),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == (
        SignalLineagePatch(
            type=SignalLineagePatchType.REWIRE_PARENTS,
            signal=A,
        ),
    )


def test_patch_builder_orders_patches_canonically():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")
    C = CanonicalSignalKey(category, "C")
    D = CanonicalSignalKey(category, "D")

    diff = SignalLineageDiff(
        added=frozenset({D}),
        removed=frozenset({A}),
        moved=frozenset({B}),
        changed_parents=frozenset({C}),
    )

    patches = build_signal_lineage_patches(diff)

    assert patches == (
        SignalLineagePatch(SignalLineagePatchType.REMOVE, A),
        SignalLineagePatch(SignalLineagePatchType.ADD, D),
        SignalLineagePatch(SignalLineagePatchType.MOVE, B),
        SignalLineagePatch(SignalLineagePatchType.REWIRE_PARENTS, C),
    )


def test_patch_builder_is_deterministic():
    category = CanonicalSignalCategory.OBSERVATION_STATE
    A = CanonicalSignalKey(category, "A")
    B = CanonicalSignalKey(category, "B")

    diff = SignalLineageDiff(
        added=frozenset({A}),
        removed=frozenset({B}),
        moved=frozenset(),
        changed_parents=frozenset(),
    )

    p1 = build_signal_lineage_patches(diff)
    p2 = build_signal_lineage_patches(diff)

    assert p1 == p2
