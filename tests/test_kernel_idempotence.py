# tests/test_kernel_idempotence.py

from __future__ import annotations

from veramem_kernel.journals.timeline.timeline_projector import project_timeline
from tests.utils import make_action


def _fingerprint(entries) -> tuple[str, ...]:
    return tuple(e.entry_id for e in entries)


def test_projection_is_idempotent_under_exact_duplicates():
    """
    Même événement injecté plusieurs fois (retries réseau, replay, etc.)
    -> projection identique à une seule occurrence, OU à défaut : stable et sans dérive.
    """
    events = [make_action(i) for i in range(10)]

    baseline = project_timeline(events=events)
    base_fp = _fingerprint(baseline)

    duplicated = events + events + events  # 3x replay
    out = project_timeline(events=duplicated)

    # Kernel industriel attendu : aucune dérive
    assert _fingerprint(out) == base_fp


def test_projection_is_idempotent_under_partial_duplicates():
    events = [make_action(i) for i in range(10)]
    baseline = project_timeline(events=events)
    base_fp = _fingerprint(baseline)

    # Simule un retry sur 3 événements
    duplicated = events + [events[2], events[5], events[7]]
    out = project_timeline(events=duplicated)

    assert _fingerprint(out) == base_fp
