"""Configuration definition."""

__all__ = ["Configuration"]

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Configuration:
    """Configuration for segwarides."""

    name: str = os.getenv("SAFIR_NAME", "segwarides")
    """The application's name, which doubles as the root HTTP endpoint path.

    Set with the ``SAFIR_NAME`` environment variable.
    """

    profile: str = os.getenv("SAFIR_PROFILE", "development")
    """Application run profile: "development" or "production".

    Set with the ``SAFIR_PROFILE`` environment variable.
    """

    logger_name: str = os.getenv("SAFIR_LOGGER", "segwarides")
    """The root name of the application's logger.

    Set with the ``SAFIR_LOGGER`` environment variable.
    """

    log_level: str = os.getenv("SAFIR_LOG_LEVEL", "INFO")
    """The log level of the application's logger.

    Set with the ``SAFIR_LOG_LEVEL`` environment variable.
    """

    credential_path: Optional[Path] = (
        None
        if os.getenv("CREDENTIAL_PATH") is None
        else Path(os.environ["CREDENTIAL_PATH"])
    )
    """Path to the location of the files with credentials.

    Set with the ``CREDENTIAL_PATH`` environment variable.
    """
