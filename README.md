# 🛒 E-Commerce Automation Framework

> A production-ready Selenium automation framework built with **Python**, **Pytest**, and the **Page Object Model (POM)** to automate an end-to-end e-commerce application.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.x-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.x-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

---

## 📌 Overview

This project automates the complete shopping workflow of the **SauceDemo** e-commerce website using modern Selenium automation practices.

It is designed with maintainability, scalability, and readability in mind, making it suitable for learning automation testing and showcasing QA engineering skills.

### 🌐 Website Under Test

https://www.saucedemo.com

---

# 🚀 Key Features

* ✅ Page Object Model (POM)
* ✅ Selenium 4 WebDriver
* ✅ Pytest Framework
* ✅ Data-Driven Testing (Excel & CSV)
* ✅ HTML Test Reports
* ✅ Automatic Screenshot on Failure
* ✅ Logging with Color Console Output
* ✅ Cross Browser Support
* ✅ End-to-End Purchase Flow
* ✅ Modular & Scalable Framework

---

# 🛠 Tech Stack

| Technology        | Purpose              |
| ----------------- | -------------------- |
| Python            | Programming Language |
| Selenium          | Browser Automation   |
| Pytest            | Test Framework       |
| WebDriver Manager | Driver Management    |
| OpenPyXL          | Excel Data Handling  |
| Pytest HTML       | HTML Reports         |
| ColorLog          | Logging              |
| Faker             | Test Data Generation |

---

# 📂 Project Structure

```text
ecommerce_automation/
│
├── config/
├── pages/
├── tests/
├── utils/
├── test_data/
├── reports/
├── logs/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── setup_windows.bat
├── run_tests.bat
└── README.md
```

---

# ✅ Test Coverage

### Authentication

* Valid Login
* Invalid Login
* Locked User
* Empty Credentials
* Logout

### Products

* Verify Product Listing
* Sort A-Z
* Sort Z-A
* Sort Price Low-High
* Sort Price High-Low

### Cart

* Add Product
* Remove Product
* Multiple Product Cart
* Cart Badge Validation

### Checkout

* Checkout Information
* Validation Messages
* Order Summary
* Order Confirmation

### End-to-End

* Complete Purchase Flow
* Multiple Item Purchase

---

# 📊 Reports

The framework automatically generates:

* HTML Report
* Failure Screenshots
* Execution Logs

```text
reports/
│── report.html
│── screenshots/

logs/
│── test_run.log
```

---

# 📈 Design Pattern

✔ Page Object Model (POM)

✔ Data-Driven Framework

✔ Utility-Based Architecture

✔ Reusable Components

✔ Explicit Wait Strategy

---

# ⚙ Installation

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-automation-framework.git

cd ecommerce-automation

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

# ▶ Run Tests

Run all tests

```bash
pytest
```

Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

Run Login Tests

```bash
pytest tests/test_login.py
```

Run Product Tests

```bash
pytest tests/test_products.py
```

Run Cart Tests

```bash
pytest tests/test_cart.py
```

Run Checkout Tests

```bash
pytest tests/test_checkout.py
```

Run End-to-End Tests

```bash
pytest tests/test_e2e.py
```

---

# 📷 Framework Highlights

* Professional Project Structure
* Easy Maintenance
* Clean Code
* Modular Design
* Real Industry Practices
* GitHub Ready
* Recruiter Friendly

---

# 📚 Future Enhancements

* Jenkins CI/CD Integration
* GitHub Actions
* Docker Support
* Parallel Execution
* Allure Reporting
* API Automation
* Database Validation

---

# 👨‍💻 Author

**Uday Anand**

GitHub: https://github.com/udayanand7

---

## ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub.
