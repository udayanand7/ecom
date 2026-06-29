"""
conftest.py – shared pytest fixtures:
  • driver  – browser session (function-scoped)
  • logged_in_driver – browser already authenticated
  • Auto-screenshot on test failure
"""

import pytest

from config.config import VALID_USERNAME, VALID_PASSWORD
from pages.login_page import LoginPage
from utils.driver_factory import get_driver
from utils.logger import get_logger
from utils.screenshot import take_screenshot

log = get_logger("conftest")


# ── Driver fixture ────────────────────────────────────────────────────────────
@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    input("Press Enter to close browser...")
    driver.quit()


# ── Pre-authenticated driver ──────────────────────────────────────────────────
@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Driver that is already logged in to SauceDemo."""
    login = LoginPage(driver)
    login.open_login_page()
    login.login(VALID_USERNAME, VALID_PASSWORD)
    login.wait_for_url_contains("inventory")
    log.info("Pre-login complete.")
    yield driver


# ── Auto screenshot on failure ────────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep     = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if drv:
            test_name = item.name.replace(" ", "_")
            path      = take_screenshot(drv, f"FAIL_{test_name}")
            log.error(f"Test FAILED – screenshot: {path}")

            # Embed screenshot in the HTML report
            if hasattr(item, "extras"):
                from pytest_html import extras as html_extras
                item.extras.append(html_extras.image(path))
