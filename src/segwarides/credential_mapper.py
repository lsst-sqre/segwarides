"""Map from services to credentials"""
from __future__ import annotations

import json
import pathlib
from typing import TYPE_CHECKING

from segwarides.config import Configuration

if TYPE_CHECKING:
    from typing import Dict

__all__ = ["make_credential_map", "get_credentials_by_key"]


def get_credentials_by_key(
    key: str, config: Configuration = None
) -> Dict[str, str]:
    if not config:
        config = Configuration()
    return make_credential_map(config)[key]


def make_credential_map(config: Configuration) -> Dict[str, Dict[str, str]]:
    path = pathlib.Path(config.credential_path)
    mapper = {}
    for f in path.iterdir():
        if f.is_dir():
            continue
        with open(f, "r") as fh:
            mapper[f.parts[-1]] = json.load(fh)
    return mapper
