"""Externally-accessible endpoint handlers that serve relative to
``/<app-name>/``.
"""

__all__ = [
    "get_index",
    "get_credentials_list",
    "get_json_credential",
]

from segwarides.handlers.external.endpoints import (
    get_credentials_list,
    get_json_credential,
)
from segwarides.handlers.external.index import get_index
