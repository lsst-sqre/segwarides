"""Map from services to credentials"""
from __future__ import annotations

import json
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
        path = self.config.credential_path
        mapper = {}
        for f in path.iterdir():
            if f.is_dir():
                continue
            try:
                mapper[f.parts[-1]] = json.loads(f.read_text())
            except json.decoder.JSONDecodeError as e:
                # This intentionally does not raise, but saves the exception
                # so that the handler can raise a useful error message if
                # the malformed credential is requested.
                # Otherwise, no credentials would be available if any
                # credential was malformed.
                mapper[f.parts[-1]] = e
        self.mapper = mapper
