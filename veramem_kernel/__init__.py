# veramem_kernel/__init__.py

from importlib.metadata import version as pkg_version
from . import api

__version__ = pkg_version("veramem-kernel")

__all__ = [
    "__version__",
    "api",
]
