"""
Driver factory – creates a configured WebDriver instance.
Supports Chrome, Firefox, and Edge.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.config import (
    BROWSER,
    HEADLESS,
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT,
    WINDOW_SIZE,
)
from utils.logger import get_logger

log = get_logger("driver_factory")


def get_driver() -> webdriver.Remote:
    browser = BROWSER.lower()
    log.info(f"Launching browser: {browser}  headless={HEADLESS}")

    if browser == "chrome":
        opts = ChromeOptions()

        if HEADLESS:
            opts.add_argument("--headless=new")

        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")
        opts.add_experimental_option("excludeSwitches", ["enable-logging"])
        opts.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()

        if HEADLESS:
            opts.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=opts,
        )

    elif browser == "edge":
        opts = EdgeOptions()

        if HEADLESS:
            opts.add_argument("--headless=new")

        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=opts,
        )

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    if WINDOW_SIZE:
        driver.set_window_size(*WINDOW_SIZE)

    log.info("Driver created successfully.")

    return driver