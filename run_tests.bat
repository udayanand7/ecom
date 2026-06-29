@echo off
REM ═══════════════════════════════════════════════════════════════
REM  Run E-Commerce Automation Tests
REM  Usage: Double-click OR open CMD and type: run_tests.bat [option]
REM  Options: all | login | products | cart | checkout | e2e
REM ═══════════════════════════════════════════════════════════════

REM Activate virtual environment
call venv\Scripts\activate.bat 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Virtual environment not found.
    echo Please run setup_windows.bat first!
    pause
    exit /b 1
)

set OPTION=%1
if "%OPTION%"=="" set OPTION=all

echo.
echo ============================================================
echo   Running: %OPTION% tests
echo ============================================================
echo.

if "%OPTION%"=="all"       pytest
if "%OPTION%"=="login"     pytest tests\test_login.py     -v
if "%OPTION%"=="products"  pytest tests\test_products.py  -v
if "%OPTION%"=="cart"      pytest tests\test_cart.py      -v
if "%OPTION%"=="checkout"  pytest tests\test_checkout.py  -v
if "%OPTION%"=="e2e"       pytest tests\test_e2e.py       -v

echo.
echo ============================================================
echo   Done! Open reports\report.html to view the HTML report.
echo ============================================================
pause
