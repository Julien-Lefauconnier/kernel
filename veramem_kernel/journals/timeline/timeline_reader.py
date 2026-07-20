# veramem_kernel/journals/timeline/timeline_reader.py

from datetime import datetime
from typing import Iterable, List, Optional

from veramem_kernel.journals.timeline.timeline_window import TimelineWindow


def _timestamp(evt):
    ts = getattr(evt, "timestamp", None)
    if ts is None:
        raise TypeError(f"Event missing timestamp: {type(evt)}")

    if not isinstance(ts, datetime):
        raise TypeError("Invalid timestamp type")

    return ts

class TimelineReader:
    """
    Kernel Timeline Reader — pure, stateless, read-only.

    Responsibilities:
    - Filter timeline events according to a TimelineWindow
    - Preserve input order
    - Never mutate events
    - Never interpret events
    """

    def read(
        self,
        *,
        events: Iterable,
        window: Optional[TimelineWindow] = None,
    ) -> List:
        """
        Read timeline events within an optional temporal window.

        Parameters:
        - events: iterable of kernel events (must expose a timestamp)
        - window: optional TimelineWindow

        Returns:
        - filtered list of events (order preserved)
        """

        if window is None:
            return list(events)

        result = []

        for evt in events:
            ts = _timestamp(evt)
            if ts.tzinfo is None:
                raise TypeError("Timeline event timestamp must be timezone-aware.")
            if ts.tzinfo.utcoffset(ts) is None:
                raise TypeError("Timeline event timestamp has invalid timezone.")
            if ts.tzinfo.utcoffset(ts).total_seconds() != 0:
                raise TypeError("Timeline event timestamp must be UTC.")

            if window.after is not None:
                if ts <= window.after.timestamp:
                    continue

            if window.before is not None:
                if ts >= window.before.timestamp:
                    continue

            result.append(evt)

        return result

