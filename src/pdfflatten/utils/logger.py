from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pdfflatten.utils.config import Config

FILE_LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] %(name)s (%(module)s:%(lineno)d): %(message)s"
)
CONSOLE_LOG_FORMAT = "[%(levelname)s] %(message)s"


def setup_logger(
    name: str = "pdfflatten",
    log_file: Path | str | None = None,
    verbose: bool = False,
) -> logging.Logger:
    """Configura y devuelve un logger con salida en consola y archivo persistente.

    Args:
        name: Nombre del logger.
        log_file: Ruta del archivo de log. Si es None, usa Config.PATHS["app_log"].
        verbose: Si es True, el handler de consola muestra nivel DEBUG; de lo contrario INFO.

    Returns:
        Instancia configurada de logging.Logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Limpiar handlers previos para evitar duplicados al reconfigurar
    if logger.handlers:
        for handler in list(logger.handlers):
            handler.close()
            logger.removeHandler(handler)

    resolved_log_file = (
        Path(log_file) if log_file is not None else Config.PATHS["app_log"]
    )
    resolved_log_file.parent.mkdir(parents=True, exist_ok=True)

    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(logging.Formatter(CONSOLE_LOG_FORMAT))
    logger.addHandler(console_handler)

    # Handler de archivo rotativo
    file_handler = RotatingFileHandler(
        resolved_log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))
    logger.addHandler(file_handler)

    return logger
