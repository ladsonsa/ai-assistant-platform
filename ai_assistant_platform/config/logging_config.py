from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

from ai_assistant_platform.config.settings import (
    LOG_BACKUP_COUNT,
    LOG_DIR,
    LOG_FILE_NAME,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_BYTES,
    LOG_TO_CONSOLE,
)

_LOGGER_NAME = "ai_assistant_platform"
_CONFIGURED_ATTR = "_ai_math_assistant_logging_configured"


def _resolve_level(level_name: str) -> int:
    """Resolves a string log level name to its corresponding logging constant.

    Args:
        level_name (str): The name of the log level (e.g., 'DEBUG', 'INFO').

    Returns:
        int: The logging level integer constant, or logging.INFO as a fallback
            if the level name is invalid.

    Raises:
        None
    """
    level = getattr(logging, level_name.upper(), None)
    if isinstance(level, int):
        return level
    return logging.INFO


def _log_file_path() -> Path:
    """Determines and creates the file path for the log file.

    Args:
        None

    Returns:
        Path: The absolute path to the log file.

    Raises:
        None
    """
    project_root = Path(__file__).resolve().parents[2]
    log_dir = project_root / LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / LOG_FILE_NAME


def configure_logging() -> logging.Logger:
    """Configures and returns the root application logger with file and optional console handlers.

    Args:
        None

    Returns:
        logging.Logger: The configured application logger instance.

    Raises:
        None
    """
    logger = logging.getLogger(_LOGGER_NAME)

    if getattr(logger, _CONFIGURED_ATTR, False):
        return logger

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    level = _resolve_level(LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        _log_file_path(),
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.setLevel(level)
    logger.propagate = False
    setattr(logger, _CONFIGURED_ATTR, True)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Retrieves a configured logger instance with the specified name.

    Args:
        name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: The requested logger instance.

    Raises:
        None
    """
    configure_logging()
    return logging.getLogger(name)
