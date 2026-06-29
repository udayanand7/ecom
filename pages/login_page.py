"""
LoginPage – https://www.saucedemo.com (landing page)
"""

from selenium.webdriver.common.by import By

from config.config import BASE_URL
from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger("login_page")


class LoginPage(BasePage):
    # ── Locators ──────────────────────────────────────────────────────────────
    USERNAME_INPUT  = (By.ID,   "user-name")
    PASSWORD_INPUT  = (By.ID,   "password")
    LOGIN_BUTTON    = (By.ID,   "login-button")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Actions ───────────────────────────────────────────────────────────────
    def open_login_page(self):
        log.info("Opening login page")
        self.open(BASE_URL)

    def enter_username(self, username: str):
        log.info(f"Entering username: {username}")
        self.type(*self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        log.info("Entering password: ****")
        self.type(*self.PASSWORD_INPUT, password)

    def click_login(self):
        log.info("Clicking login button")
        self.click(*self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Full login action."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Verifications ─────────────────────────────────────────────────────────
    def get_error_message(self) -> str:
        return self.get_text(*self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(*self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        return "saucedemo.com" in self.current_url and \
               "inventory" not in self.current_url
