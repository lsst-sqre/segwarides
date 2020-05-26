"""Map from services to credentials"""
from __future__ import annotations

import json
import pathlib
from collections.abc import Mapping
from typing import TYPE_CHECKING

from segwarides.config import Configuration

if TYPE_CHECKING:
    from typing import (
        Dict,
        Iterator,
        ValuesView,
        KeysView,
        ItemsView,
    )

__all__ = ["CredentialMapper"]


class CredentialMapper(Mapping):
    def __init__(self, config: Configuration) -> None:
        self.config = config
        self._refresh()

    def __getitem__(self, key: str) -> Dict[str, str]:
        self._refresh()
        return self.mapper[key]

    def __iter__(self) -> Iterator:
        self._refresh()
        return iter(self.mapper)

    def values(self) -> ValuesView:
        self._refresh()
        return self.mapper.values()

    def keys(self) -> KeysView:
        self._refresh()
        return self.mapper.keys()

    def items(self) -> ItemsView[str, Dict[str, str]]:
        self._refresh()
        return self.mapper.items()

    def __len__(self) -> int:
        self._refresh()
        return len(self.mapper)

    def _refresh(self) -> None:
        path = pathlib.Path(self.config.credential_path)
        mapper = {}
        for f in path.iterdir():
            if f.is_dir():
                continue
            with open(f, "r") as fh:
                try:
                    mapper[f.parts[-1]] = json.load(fh)
                except json.decoder.JSONDecodeError as e:
                    mapper[f.parts[-1]] = e
        self.mapper = mapper
