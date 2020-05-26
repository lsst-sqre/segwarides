"""The main application definition for segwarides service."""

__all__ = ["create_app"]

from typing import Any

from aiohttp import web
from safir.http import init_http_session
from safir.logging import configure_logging
from safir.metadata import setup_metadata
from safir.middleware import bind_logger

from segwarides.config import Configuration
from segwarides.credential_mapper import CredentialMapper
from segwarides.handlers import init_external_routes, init_internal_routes


def create_app(**configs: Any) -> web.Application:
    """Create and configure the aiohttp.web application."""
    config = Configuration(**configs)
    configure_logging(
        profile=config.profile,
        log_level=config.log_level,
        name=config.logger_name,
    )

    mapper = CredentialMapper(config)

    root_app = web.Application()
    root_app["safir/config"] = config
    root_app["segwarides/creds_mapper"] = mapper
    setup_metadata(package_name="segwarides", app=root_app)
    setup_middleware(root_app)
    root_app.add_routes(init_internal_routes())
    root_app.cleanup_ctx.append(init_http_session)

    sub_app = web.Application()
    setup_middleware(sub_app)
    sub_app.add_routes(init_external_routes())
    root_app.add_subapp(f'/{root_app["safir/config"].name}', sub_app)

    return root_app


def setup_middleware(app: web.Application) -> None:
    """Add middleware to the application."""
    app.middlewares.append(bind_logger)
