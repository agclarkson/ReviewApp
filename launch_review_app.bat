@echo off
echo ========================================
echo ORRA Referee Review System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if openpyxl is installed
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installing required library...
    python -m pip install openpyxl
    if errorlevel 1 (
        echo ERROR: Failed to install openpyxl
        echo Please run: pip install openpyxl
        pause
        exit /b 1
    )
)

echo Starting Referee Review System...
echo.
python referee_review_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    pause
)
