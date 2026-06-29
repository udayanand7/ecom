"""
Tests for login / authentication.
Data-driven: reads users from test_data/users.xlsx
"""

import pytest

from config.config import (
    VALID_USERNAME, VALID_PASSWORD,
    LOCKED_USERNAME, INVALID_USERNAME, INVALID_PASSWORD,
    USERS_EXCEL,
)
from pages.login_page    import LoginPage
from pages.products_page import ProductsPage
from utils.data_reader   import read_excel
from utils.logger        import get_logger

log = get_logger("test_login")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _login_page(driver) -> LoginPage:
    page = LoginPage(driver)
    page.open_login_page()
    return page


# ── 1. Valid login ────────────────────────────────────────────────────────────
class TestValidLogin:
    def test_login_success(self, driver):
        """Standard_user can log in and reach the inventory page."""
        login = _login_page(driver)
        login.login(VALID_USERNAME, VALID_PASSWORD)
        login.wait_for_url_contains("inventory")

        products = ProductsPage(driver)
        assert products.is_on_products_page(), "Should be on inventory page"
        assert products.get_page_title() == "Products"
        log.info("PASS: valid login → inventory page")

    def test_logout(self, logged_in_driver):
        """User can log out successfully."""
        products = ProductsPage(logged_in_driver)
        products.logout()
        login = LoginPage(logged_in_driver)
        assert login.is_login_page(), "Should be back on login page"
        log.info("PASS: logout works")


# ── 2. Invalid login ──────────────────────────────────────────────────────────
class TestInvalidLogin:
    def test_wrong_password(self, driver):
        login = _login_page(driver)
        login.login(VALID_USERNAME, INVALID_PASSWORD)
        assert login.is_error_displayed(), "Error should be shown"
        assert "Username and password do not match" in login.get_error_message()

    def test_wrong_username(self, driver):
        login = _login_page(driver)
        login.login(INVALID_USERNAME, VALID_PASSWORD)
        assert login.is_error_displayed()

    def test_empty_credentials(self, driver):
        login = _login_page(driver)
        login.click_login()
        assert login.is_error_displayed()
        assert "Username is required" in login.get_error_message()

    def test_locked_user(self, driver):
        login = _login_page(driver)
        login.login(LOCKED_USERNAME, VALID_PASSWORD)
        assert login.is_error_displayed()
        assert "locked out" in login.get_error_message().lower()


# ── 3. Data-driven login from Excel ──────────────────────────────────────────
def get_user_test_data():
    """Load rows from users.xlsx → parametrize."""
    rows = read_excel(USERS_EXCEL)
    if not rows:
        # Fallback so tests can still run without the file
        return [
            ("standard_user", "secret_sauce", True),
            ("locked_out_user", "secret_sauce", False),
            ("invalid_user", "wrong_pass", False),
        ]
    return [(r["username"], r["password"], str(r["expected_login"]).lower() == "true")
            for r in rows]


@pytest.mark.parametrize("username,password,should_pass", get_user_test_data())
def test_login_data_driven(driver, username, password, should_pass):
    """Data-driven test using users.xlsx."""
    login = LoginPage(driver)
    login.open_login_page()
    login.login(username, password)

    if should_pass:
        login.wait_for_url_contains("inventory")
        assert ProductsPage(driver).is_on_products_page()
        log.info(f"PASS: {username} logged in")
    else:
        assert login.is_error_displayed(), \
            f"Expected error for user '{username}' but none shown"
        log.info(f"PASS: {username} correctly rejected")
