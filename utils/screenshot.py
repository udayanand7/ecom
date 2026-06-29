"""
Screenshot helper – captures a timestamped PNG on demand or on failure.
"""

import os
from datetime import datetime

from config.config import SCREENSHOTS_DIR
from utils.logger import get_logger

log = get_logger("screenshot")


def take_screenshot(driver, name: str = "screenshot") -> str:
    """
    Save a screenshot and return its absolute path.
    Called automatically by conftest on test failure.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"{name}_{timestamp}.png"
    filepath  = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        log.info(f"Screenshot saved → {filepath}")
    except Exception as exc:
        log.error(f"Screenshot failed: {exc}")

    return filepath
