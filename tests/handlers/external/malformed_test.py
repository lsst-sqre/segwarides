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


async def test_get_malformed_json(aiohttp_client: TestClient) -> None:
    """Test GET /segwarides/creds/cred3"""
    app = create_app()
    name = app["safir/config"].name
    client = await aiohttp_client(app)

    response = await client.get(f"/{name}/creds/cred3")
    text = await response.text()
    assert response.status == 500
    assert text == "Unable to decode credentials JSON document"
