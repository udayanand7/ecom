"""
Colored console + rotating file logger.
Usage:
    from utils.logger import get_logger
    log = get_logger(__name__)
    log.info("step started")
"""

import logging
import os
from logging.handlers import RotatingFileHandler

import colorlog

from config.config import LOG_FILE, LOGS_DIR


def get_logger(name: str = "ecommerce") -> logging.Logger:
    os.makedirs(LOGS_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:          # avoid duplicate handlers on re-import
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Console handler (colored) ─────────────────────────────────────────────
    console_fmt = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)-8s] %(name)s :: %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        },
    )
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(console_fmt)

    # ── File handler (rotating, plain text) ───────────────────────────────────
    file_fmt = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(file_fmt)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
