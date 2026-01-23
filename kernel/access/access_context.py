# kernel/access/access_context.py

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AccessContext:
    """
    Kernel-level access context.

    - Declarative
    - Immutable
    - No inference
    """

    user_id: str
    place_id: Optional[str] = None
