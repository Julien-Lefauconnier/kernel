# tests/test_kernel_commutativity.py

from __future__ import annotations

import itertools
import random

from veramem_kernel.journals.timeline.timeline_projector import project_timeline

from tests.utils import make_action


def _fingerprint(entries) -> tuple[str, ...]:
    """
    Fingerprint canonique stable :
    on compare sur entry_id (ou autre identifiant stable).
    """
    return tuple(e.entry_id for e in entries)


def test_projection_is_commutative_for_small_permutations():
    """
    Pour un petit set (N=5), on peut tester TOUTES les permutations.
    Objectif : le projector doit être invariant à l'ordre d'entrée.
    """
    events = [make_action(i) for i in range(5)]

    baseline = project_timeline(events=events)
    base_fp = _fingerprint(baseline)

    for perm in itertools.permutations(events):
        out = project_timeline(events=list(perm))
        assert _fingerprint(out) == base_fp


def test_projection_is_commutative_under_seeded_shuffles():
    """
    Fuzz déterministe : on shuffle 200 fois avec une seed fixe.
    """
    events = [make_action(i) for i in range(20)]
    baseline = project_timeline(events=events)
    base_fp = _fingerprint(baseline)

    rng = random.Random(1337)

    for _ in range(200):
        perm = list(events)
        rng.shuffle(perm)
        out = project_timeline(events=perm)
        assert _fingerprint(out) == base_fp
