@echo off
echo ========================================
echo   Billionaire Path Bot - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo.
    echo Please create .env file with your API keys
    echo See .env.example for reference
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import telegram" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    echo.
    pip install -r requirements.txt
    echo.
)

echo Starting bot...
echo.
echo Bot is running. Keep this window open.
echo Press Ctrl+C to stop the bot.
echo.
echo ========================================
echo.

python billionaire-path-bot.py

pause
