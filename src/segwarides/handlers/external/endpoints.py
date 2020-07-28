"""Handlers for credentials information endpoints."""

__all__ = [
    "get_credentials_list",
    "get_json_credential",
]

import json

from aiohttp import web

from segwarides.handlers import routes


@routes.get("/list")
async def get_credentials_list(request: web.Request) -> web.Response:
    """GET list of the keys for credentials stored in this service.

    Response is a JSON list of valid keys to use with this service.
    """
    credentials_map = request.config_dict["segwarides/creds_mapper"]
    return web.json_response(
        [
            k
            for k, v in credentials_map.items()
            if not isinstance(v, json.decoder.JSONDecodeError)
        ]
    )


@routes.get("/creds/{credential_key}")
async def get_json_credential(request: web.Request) -> web.Response:
    """GET credentials associated with a particular key

    Response is a JSON dict containing the credentials if the key
    corresponds to valid credentials.  Otherwise, returns 404.
    """
    key = request.match_info["credential_key"]
    try:
        creds = request.config_dict["segwarides/creds_mapper"][key]
        if isinstance(creds, json.decoder.JSONDecodeError):
            msg = "Unable to decode credentials JSON document"
            return web.Response(status=500, text=msg)
        return web.json_response(creds)
    except KeyError:
        msg = f"No credentials for {key}."
        return web.Response(status=404, text=msg)
