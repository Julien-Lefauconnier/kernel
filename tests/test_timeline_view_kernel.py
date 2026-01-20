# tests/test_timeline_view_kernel.py

import pytest
from datetime import datetime
from uuid import uuid4

from kernel.journals.timeline.timeline_entry import (
    TimelineEntry,
    TimelineEntryNature,
)
from kernel.journals.timeline.timeline_types import TimelineEntryType
from kernel.journals.timeline.timeline_view import TimelineView
from kernel.journals.timeline.timeline_view_builder import TimelineViewBuilder
from kernel.journals.timeline.timeline_view_types import TimelineViewRole


def make_entry(entry_type, *, nature=TimelineEntryNature.EVENT):
    return TimelineEntry(
        entry_id=str(uuid4()),
        created_at=datetime.utcnow(),
        type=entry_type,
        title=entry_type.value,
        description=None,
        action_id=None,
        place_id=None,
        nature=nature,
    )


# -------------------------------------------------
# Basic construction
# -------------------------------------------------

def test_build_trace_factuelle_view_filters_event_types():
    entries = [
        make_entry(TimelineEntryType.ACTION_PROPOSED),
        make_entry(TimelineEntryType.CONFLICT),
        make_entry(TimelineEntryType.DOCUMENT_EDITED),
        make_entry(TimelineEntryType.REASONING_GAP, nature=TimelineEntryNature.STATE),
    ]

    view = TimelineViewBuilder.build(
        role=TimelineViewRole.TRACE_FACTUELLE,
        entries=entries,
    )

    assert isinstance(view, TimelineView)
    assert view.role == TimelineViewRole.TRACE_FACTUELLE

    # Only factual events
    assert all(
        e.type in {
            TimelineEntryType.ACTION_PROPOSED,
            TimelineEntryType.DOCUMENT_EDITED,
        }
        for e in view.entries
    )


def test_build_state_view_only_contains_state_entries():
    entries = [
        make_entry(TimelineEntryType.ACTION_PROPOSED),
        make_entry(TimelineEntryType.REASONING_GAP, nature=TimelineEntryNature.STATE),
        make_entry(TimelineEntryType.UNCERTAINTY_FRAME, nature=TimelineEntryNature.STATE),
    ]

    view = TimelineViewBuilder.build(
        role=TimelineViewRole.ETAT_COGNITIF_SYSTEME,
        entries=entries,
    )

    assert all(e.nature == TimelineEntryNature.STATE for e in view.entries)


# -------------------------------------------------
# Ordering & immutability
# -------------------------------------------------

def test_view_preserves_entry_order():
    e1 = make_entry(TimelineEntryType.ACTION_PROPOSED)
    e2 = make_entry(TimelineEntryType.DOCUMENT_ACCESSED)

    view = TimelineViewBuilder.build(
        role=TimelineViewRole.TRACE_FACTUELLE,
        entries=[e1, e2],
    )

    assert view.entries[0] == e1
    assert view.entries[1] == e2


def test_view_is_immutable():
    entry = make_entry(TimelineEntryType.ACTION_PROPOSED)

    view = TimelineViewBuilder.build(
        role=TimelineViewRole.TRACE_FACTUELLE,
        entries=[entry],
    )

    with pytest.raises(Exception):
        view.entries += (entry,)


# -------------------------------------------------
# build_all
# -------------------------------------------------

def test_build_all_returns_one_view_per_role():
    entries = [
        make_entry(TimelineEntryType.ACTION_PROPOSED),
        make_entry(TimelineEntryType.REASONING_GAP, nature=TimelineEntryNature.STATE),
    ]

    views = TimelineViewBuilder.build_all(entries=entries)

    roles = {v.role for v in views}

    assert roles == set(TimelineViewRole)
