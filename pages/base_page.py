"""
BasePage – all Page Objects inherit from this class.
Provides reusable wrappers around Selenium interactions with built-in
explicit waits, logging, and error handling.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC
from selenium.webdriver.common.by  import By
from selenium.common.exceptions    import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException
)

from config.config import IMPLICIT_WAIT
from utils.logger  import get_logger

log = get_logger("base_page")


class BasePage:
    def __init__(self, driver):
        self.driver  = driver
        self.wait    = WebDriverWait(driver, IMPLICIT_WAIT)

    # ── Navigation ────────────────────────────────────────────────────────────
    def open(self, url: str):
        log.info(f"Navigating to: {url}")
        self.driver.get(url)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    # ── Finders ───────────────────────────────────────────────────────────────
    def find(self, by: By, locator: str):
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            log.error(f"Element not found: {by}='{locator}'")
            raise

    def find_all(self, by: By, locator: str):
        return self.driver.find_elements(by, locator)

    def find_clickable(self, by: By, locator: str):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def find_visible(self, by: By, locator: str):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    # ── Actions ───────────────────────────────────────────────────────────────
    def click(self, by: By, locator: str):
        log.debug(f"Clicking: {by}='{locator}'")
        try:
            self.find_clickable(by, locator).click()
        except ElementClickInterceptedException:
            # JS fallback
            el = self.find(by, locator)
            self.driver.execute_script("arguments[0].click();", el)

    def type(self, by: By, locator: str, text: str):
        log.debug(f"Typing '{text}' into: {by}='{locator}'")
        el = self.find(by, locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, by: By, locator: str) -> str:
        return self.find(by, locator).text.strip()

    def is_displayed(self, by: By, locator: str) -> bool:
        try:
            return self.find_visible(by, locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, fragment: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(fragment)
        )

    def scroll_to(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )
