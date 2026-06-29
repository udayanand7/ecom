# 🛒 E-Commerce Automation Framework

A **production-grade** Selenium + pytest automation framework targeting [SauceDemo](https://www.saucedemo.com) — a free, purpose-built demo e-commerce site perfect for automation practice.

---

## ✅ Features

| Feature | Details |
|---|---|
| **Login / Logout** | Valid, invalid, locked-user, empty-field scenarios |
| **Product Listing** | Sort A→Z, Z→A, Price Low→High, Price High→Low |
| **Cart Management** | Add by name, add first-N, remove, empty cart |
| **Checkout Flow** | Step 1 (info), Step 2 (review), Order Confirmation |
| **End-to-End Tests** | Full user journey in a single test |
| **Screenshot on Failure** | Auto-captures PNG and embeds in HTML report |
| **HTML Reports** | Self-contained `reports/report.html` |
| **Logging** | Colored console + rotating file logs |
| **Page Object Model** | Clean separation of locators and actions |
| **Data-Driven Testing** | Excel (`users.xlsx`, `checkout_data.xlsx`) + CSV (`products.csv`) |

---

## 🌐 Target Site

**URL:** `https://www.saucedemo.com`

| Username | Password | Status |
|---|---|---|
| `standard_user` | `secret_sauce` | ✅ Works |
| `locked_out_user` | `secret_sauce` | 🔒 Locked |
| `problem_user` | `secret_sauce` | ✅ Works (with quirks) |
| `performance_glitch_user` | `secret_sauce` | ✅ Works (slow) |

---

## 🖥️ Windows Setup – Step by Step

### Prerequisites

**1. Install Python 3.9+**
- Go to: https://www.python.org/downloads/
- Download **Python 3.11** (recommended)
- During installation, **check the box ✅ "Add Python to PATH"**
- Verify in CMD:
  ```
  python --version
  ```
  Should print something like: `Python 3.11.x`

**2. Install Google Chrome**
- Download from: https://www.google.com/chrome/
- `webdriver-manager` will automatically download the matching ChromeDriver — no manual setup needed

**3. Install Git (optional, for GitHub)**
- Download from: https://git-scm.com/downloads
- Use all default settings during install

---

### Installation

**Step 1 – Extract the zip**
- Right-click the downloaded zip → **Extract All**
- Choose a folder, e.g.: `C:\Users\YourName\ecommerce_automation`

**Step 2 – Open Command Prompt in that folder**
- Open File Explorer → navigate to the extracted folder
- Click the address bar → type `cmd` → press Enter
  *(This opens CMD already in that folder)*

**Step 3 – Run the setup script**
```cmd
setup_windows.bat
```
This will:
- ✅ Check Python is installed
- ✅ Create a virtual environment (`venv\`)
- ✅ Install all dependencies from `requirements.txt`
- ✅ Create `reports\screenshots\` and `logs\` folders

---

## ▶️ Running Tests

Activate the virtual environment first (if not already done):
```cmd
venv\Scripts\activate
```

### Run all tests
```cmd
pytest
```

### Run with HTML report
```cmd
pytest --html=reports\report.html --self-contained-html
```

### Run a specific test file
```cmd
pytest tests\test_login.py -v
pytest tests\test_products.py -v
pytest tests\test_cart.py -v
pytest tests\test_checkout.py -v
pytest tests\test_e2e.py -v
```

### Run a single test
```cmd
pytest tests\test_e2e.py::TestFullJourney::test_complete_purchase_flow -v
```

### Use the helper batch file
```cmd
run_tests.bat           # Run all tests
run_tests.bat e2e       # Run only E2E tests
run_tests.bat login     # Run only login tests
run_tests.bat cart      # Run only cart tests
run_tests.bat checkout  # Run only checkout tests
```

---

## 📁 Project Structure

```
ecommerce_automation/
│
├── config/
│   └── config.py              ← All settings (URL, browser, timeouts, credentials)
│
├── pages/                     ← Page Object Model (POM)
│   ├── base_page.py           ← Shared Selenium helpers (click, type, wait…)
│   ├── login_page.py          ← Login page locators & actions
│   ├── products_page.py       ← Inventory/products page
│   ├── cart_page.py           ← Shopping cart page
│   └── checkout_page.py       ← Step 1, Step 2, Confirmation pages
│
├── tests/
│   ├── test_login.py          ← Login / auth tests (data-driven via Excel)
│   ├── test_products.py       ← Sort & filter tests (data-driven via CSV)
│   ├── test_cart.py           ← Add/remove cart tests
│   ├── test_checkout.py       ← Checkout form & flow tests (data-driven)
│   └── test_e2e.py            ← Full end-to-end journey tests
│
├── utils/
│   ├── driver_factory.py      ← Creates Chrome/Firefox/Edge WebDriver
│   ├── logger.py              ← Colored console + rotating file logger
│   ├── screenshot.py          ← Auto screenshot on failure
│   └── data_reader.py         ← Read Excel (.xlsx) and CSV files
│
├── test_data/
│   ├── users.xlsx             ← Usernames, passwords, expected outcome
│   ├── checkout_data.xlsx     ← First name, last name, zip, expected outcome
│   └── products.csv           ← Expected product names and prices
│
├── reports/
│   ├── report.html            ← HTML test report (generated after run)
│   └── screenshots/           ← Auto-captured failure screenshots
│
├── logs/
│   └── test_run.log           ← Rotating log file
│
├── conftest.py                ← Shared fixtures + auto-screenshot on failure
├── pytest.ini                 ← pytest configuration
├── requirements.txt           ← Python dependencies
├── setup_windows.bat          ← One-click Windows setup
└── run_tests.bat              ← Helper to run tests from CMD
```

---

## ⚙️ Configuration

Edit `config/config.py` to change settings:

```python
BROWSER   = "chrome"   # Options: "chrome", "firefox", "edge"
HEADLESS  = False      # True = no visible browser window (faster CI)
```

---

## 📊 Test Data Files

### `test_data/users.xlsx` — Login scenarios
| username | password | expected_login |
|---|---|---|
| standard_user | secret_sauce | True |
| locked_out_user | secret_sauce | False |
| invalid_user | wrong_pass | False |

### `test_data/checkout_data.xlsx` — Checkout form validation
| first_name | last_name | zip_code | should_pass |
|---|---|---|---|
| Alice | Smith | 10001 | True |
| | Brown | 30003 | False |

### `test_data/products.csv` — Expected product catalogue
| product_name | expected_price |
|---|---|
| Sauce Labs Backpack | 29.99 |
| Sauce Labs Bike Light | 9.99 |

---

## 📋 HTML Report

After running tests, open:
```
reports\report.html
```
Double-click it in File Explorer — it opens in your browser and shows:
- ✅ / ❌ Pass/Fail for each test
- Duration per test
- Embedded failure screenshots
- Full console log

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `python` not recognized | Re-install Python and check "Add to PATH" |
| `ChromeDriver` error | `webdriver-manager` auto-installs it; ensure Chrome is up-to-date |
| `ModuleNotFoundError` | Run `venv\Scripts\activate` then `pip install -r requirements.txt` |
| Tests fail with timeout | Increase `IMPLICIT_WAIT` in `config.py` or check internet connection |
| Browser window flashes and closes | Normal during test run; check `reports\report.html` for results |

---

## 🐙 GitHub – Push Your Project

```bash
git init
git add .
git commit -m "Initial commit: E-Commerce Automation Framework"
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-automation.git
git push -u origin main
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `selenium` | Browser automation |
| `pytest` | Test runner |
| `pytest-html` | HTML test reports |
| `openpyxl` | Read/write Excel files |
| `webdriver-manager` | Auto-downloads ChromeDriver/GeckoDriver |
| `colorlog` | Colored console logging |
| `Faker` | Generate fake test data (optional use) |
