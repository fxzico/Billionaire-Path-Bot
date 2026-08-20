@echo off
echo ========================================
echo   Installing Billionaire Path Bot
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

echo Python found. Installing dependencies...
echo.

pip install -r requirements.txt

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open .env file in Notepad
echo 2. Add your Anthropic API key (get from https://console.anthropic.com/settings/keys)
echo 3. Double-click START_BOT.bat to run your bot
echo.
pause
