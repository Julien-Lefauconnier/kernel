# kernel/journals/timeline/timeline_view_types.py

from enum import Enum


class TimelineViewRole(str, Enum):
    """
    Canonical timeline view roles.

    Kernel-level roles are purely declarative.
    No access policy, no interpretation.
    """

    TRACE_FACTUELLE = "trace_factuelle"
    ETAT_COGNITIF_SYSTEME = "etat_cognitif_systeme"
    AWARENESS_POST_COGNITIVE = "awareness_post_cognitive"
    GOUVERNANCE_HUMAINE = "gouvernance_humaine"
