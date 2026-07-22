# app/core/logger.py
"""
ARGUS Logging System
====================
Replaces print() statements with a proper logging system.

Why: Production systems need structured logs with timestamps,
     severity levels, and the ability to save to files.
"""

import logging
import sys
from app.core.config import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger instance.

    Usage in any file:
        from app.core.logger import setup_logger
        logger = setup_logger(__name__)
        logger.info("Something happened")
        logger.warning("Watch out")
        logger.error("Something broke")
    """

    logger = logging.getLogger(name)

    # Set level based on debug mode
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(level)

    # Don't add handlers if they already exist
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Format: timestamp [LEVEL] module_name: message
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Main ARGUS logger
logger = setup_logger("ARGUS")