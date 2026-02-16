# kernel/kernel/journals/timeline/timeline_source.py
from typing import Protocol
from datetime import datetime


class TimelineSourceEvent(Protocol):
    created_at: datetime
