"""
Central configuration file for the E-Commerce Automation Framework.
Target site: https://www.saucedemo.com (free demo e-commerce site)
"""

import os

# ── Base URL ──────────────────────────────────────────────────────────────────
BASE_URL = "https://www.saucedemo.com"

# ── Browser settings ──────────────────────────────────────────────────────────
BROWSER          = "chrome"   # chrome | firefox | edge
HEADLESS         = False      # True = run without visible window
IMPLICIT_WAIT    = 10         # seconds
PAGE_LOAD_TIMEOUT = 30        # seconds
WINDOW_SIZE      = (1366, 768)

# ── Credentials (SauceDemo built-in test accounts) ────────────────────────────
VALID_USERNAME   = "standard_user"
VALID_PASSWORD   = "secret_sauce"
LOCKED_USERNAME  = "locked_out_user"
INVALID_USERNAME = "invalid_user"
INVALID_PASSWORD = "wrong_password"

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR      = os.path.join(ROOT_DIR, "reports")
SCREENSHOTS_DIR  = os.path.join(REPORTS_DIR, "screenshots")
LOGS_DIR         = os.path.join(ROOT_DIR, "logs")
TEST_DATA_DIR    = os.path.join(ROOT_DIR, "test_data")

# ── Test data files ───────────────────────────────────────────────────────────
USERS_EXCEL      = os.path.join(TEST_DATA_DIR, "users.xlsx")
PRODUCTS_CSV     = os.path.join(TEST_DATA_DIR, "products.csv")
CHECKOUT_EXCEL   = os.path.join(TEST_DATA_DIR, "checkout_data.xlsx")

# ── Report ────────────────────────────────────────────────────────────────────
HTML_REPORT      = os.path.join(REPORTS_DIR, "report.html")
LOG_FILE         = os.path.join(LOGS_DIR, "test_run.log")
