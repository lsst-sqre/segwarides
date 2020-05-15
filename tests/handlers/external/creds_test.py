"""Tests for the segwarides.handlers.external.index module and routes."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from segwarides.app import create_app

if TYPE_CHECKING:
    from aiohttp.pytest_plugin.test_utils import TestClient


async def test_get_creds(aiohttp_client: TestClient) -> None:
    """Test GET /segwarides/creds"""
    app = create_app(credential_path=str(Path(__file__).parents[1] / "secret"))
    name = app["safir/config"].name
    client = await aiohttp_client(app)
    expected = {
        "cred1": {
            "username": "foo",
            "password": "bar",
            "endpoint": "somewhere.on/the/web",
        },
        "cred2": {
            "token": "ae01453bc3221455fd",
            "endpoint": "somewhere.else.on/the/web",
        },
    }
    for cred in ["cred1", "cred2"]:
        response = await client.get(f"/{name}/creds/{cred}")
        assert response.status == 200
        data = await response.json()
        for k in expected[cred]:
            assert expected[cred][k] == data[k]
