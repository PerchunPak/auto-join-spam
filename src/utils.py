"""Module for some useful utils."""

import re
import os
import pathlib
import sys
import typing as t

from loguru import logger

BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = pathlib.Path(os.environ.get("DATA_DIR", BASE_DIR / "data"))


class Singleton(type):
    """Metaclass to do Singleton pattern."""

    _instances: dict[type, t.Any] = {}  # type: ignore[misc] # Explicit "Any" is not allowed

    def __call__(cls, *args, **kwargs) -> t.Any:  # type: ignore[misc] # Explicit "Any" is not allowed
        """Actual logic in this class.

        See https://stackoverflow.com/a/6798042.
        """
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)

            if hasattr(instance, "_setup"):
                instance = instance._setup()
            cls._instances[cls] = instance

        return cls._instances[cls]


def validate_link(link: str) -> bool:
    result = re.match(r".*(t\.me/)?(\+[\d\w_-]{16})$", link)
    if result:
        return result.group(2)
    return False


def setup_logging() -> None:
    """Setup logging for the addon."""
    from src import config as config_module  # circular import

    config = config_module.Config()

    logger.remove()
    if config.logging.level < config_module.LoggingLevel.WARNING:
        logger.add(
            sys.stdout,
            level=config.logging.level,
            filter=lambda record: record["level"].no
            < config_module.LoggingLevel.WARNING,
            colorize=True,
            serialize=config.logging.json,
            backtrace=True,
            diagnose=True,
        )
    logger.add(
        sys.stderr,
        level=config.logging.level,
        filter=lambda record: record["level"].no >= config_module.LoggingLevel.WARNING,
        colorize=True,
        serialize=config.logging.json,
        backtrace=True,
        diagnose=True,
    )
    logger.debug("Logging was setup!")
