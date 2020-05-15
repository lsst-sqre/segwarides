"""Tests for the segwarides.handlers.external.index module and routes."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from segwarides.app import create_app

# Set up path to test credentials
os.environ["CREDENTIAL_PATH"] = str(Path(__file__).parents[1] / "secret")


if TYPE_CHECKING:
    from aiohttp.pytest_plugin.test_utils import TestClient


async def test_get_list(aiohttp_client: TestClient) -> None:
    """Test GET /segwarides/list"""
    app = create_app()
    name = app["safir/config"].name
    client = await aiohttp_client(app)

    expected = ["cred1", "cred2"]

    response = await client.get(f"/{name}/list")
    assert response.status == 200
    data = await response.json()
    for el in expected:
        assert el in data
