# kernel/journals/timeline/timeline_reader.py

from typing import Iterable, List, Optional

from kernel.journals.timeline.timeline_window import TimelineWindow


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
            ts = evt.created_at

            if window.after is not None:
                if ts <= window.after.timestamp:
                    continue

            if window.before is not None:
                if ts >= window.before.timestamp:
                    continue

            result.append(evt)

        return result
