"""Tests for the segwarides.handlers.internal.index module and routes.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from segwarides.app import create_app

if TYPE_CHECKING:
    from aiohttp.pytest_plugin.test_utils import TestClient


async def test_get_index(aiohttp_client: TestClient) -> None:
    """Test GET /"""
    app = create_app(credential_path=Path(__file__).parents[1] / "secret")
    client = await aiohttp_client(app)

    response = await client.get("/")
    assert response.status == 200
    data = await response.json()
    assert data["name"] == app["safir/config"].name
    assert isinstance(data["version"], str)
    assert isinstance(data["description"], str)
    assert isinstance(data["repository_url"], str)
    assert isinstance(data["documentation_url"], str)
