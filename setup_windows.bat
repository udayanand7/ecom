@echo off
REM ═══════════════════════════════════════════════════════════════
REM  E-Commerce Automation Framework – Windows Setup Script
REM  Run this ONCE after extracting the zip file.
REM ═══════════════════════════════════════════════════════════════

echo.
echo ============================================================
echo   E-Commerce Automation Framework - Setup
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
echo [OK] Python found:
python --version

REM Check pip
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip not found. Reinstall Python with pip included.
    pause
    exit /b 1
)
echo [OK] pip found.

REM Create virtual environment
echo.
echo [1/4] Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment created.

REM Activate venv
echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated.

REM Install dependencies
echo.
echo [3/4] Installing dependencies (this may take a minute)...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] All dependencies installed.

REM Create required directories
echo.
echo [4/4] Creating required directories...
if not exist "reports\screenshots" mkdir reports\screenshots
if not exist "logs"                mkdir logs
echo [OK] Directories ready.

echo.
echo ============================================================
echo   SETUP COMPLETE!
echo ============================================================
echo.
echo   To run tests, use one of the following commands:
echo.
echo   Run ALL tests:
echo     venv\Scripts\activate ^& pytest
echo.
echo   Run with HTML report:
echo     pytest --html=reports\report.html --self-contained-html
echo.
echo   Run only E2E tests:
echo     pytest tests\test_e2e.py -v
echo.
echo   Run only login tests:
echo     pytest tests\test_login.py -v
echo.
echo   Run headless (no browser window):
echo     Uncomment HEADLESS = True in config\config.py
echo.
echo ============================================================
pause
