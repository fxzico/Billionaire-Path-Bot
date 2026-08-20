@echo off
echo.
echo ========================================
echo   AUTOMATED RENDER DEPLOYMENT
echo   Billionaire Path Bot - Lifetime Free
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git\" (
    echo [1/6] Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - Billionaire Path Bot"
) else (
    echo [1/6] Git repository already initialized
)

REM Check if GitHub repo exists
echo.
echo [2/6] Checking GitHub repository...
git remote -v | findstr "origin" >nul 2>&1
if errorlevel 1 (
    echo.
    echo GitHub repository needed for Render deployment.
    echo.
    set /p CREATE_REPO="Create GitHub repo automatically? (y/n): "
    if /i "%CREATE_REPO%"=="y" (
        echo.
        echo Creating GitHub repository...
        gh repo create Billionaire-Path-Bot --public --source=. --remote=origin --push
        if errorlevel 1 (
            echo.
            echo ERROR: GitHub CLI not installed or not logged in.
            echo.
            echo Please install GitHub CLI: https://cli.github.com/
            echo Then run: gh auth login
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Please create a GitHub repo manually at: https://github.com/new
        echo Then run: git remote add origin https://github.com/YOUR_USERNAME/Billionaire-Path-Bot.git
        echo Then run: git push -u origin main
        pause
        exit /b 1
    )
) else (
    echo GitHub remote found
    echo Pushing latest changes...
    git add .
    git commit -m "Update for Render deployment" >nul 2>&1
    git push origin main
)

echo.
echo [3/6] Opening Render dashboard...
start https://dashboard.render.com/

echo.
echo ========================================
echo   MANUAL STEPS (2 minutes)
echo ========================================
echo.
echo In the Render dashboard that just opened:
echo.
echo 1. Click "New +" button (top right)
echo 2. Select "Web Service"
echo 3. Click "Connect Repository"
echo 4. Authorize GitHub (if asked)
echo 5. Select "Billionaire-Path-Bot" repository
echo 6. Click "Connect"
echo.
echo Configuration will auto-fill from render.yaml, then:
echo.
echo 7. Scroll to "Environment Variables" section
echo 8. Add these TWO variables:
echo.
echo    Key: TELEGRAM_BOT_TOKEN
echo    Value: [Get from .env file in your project folder]
echo.
echo    Key: ANTHROPIC_API_KEY
echo    Value: [Get from .env file in your project folder]
echo.
echo 9. Click "Create Web Service"
echo.
echo 10. Wait 3-5 minutes for deployment
echo.
echo ========================================
echo.
echo After deployment completes:
echo - Open Telegram
echo - Search: @Zico_Billionaire_Path_bot
echo - Send: /start
echo - Send: /log Today I worked 5 hours on my business
echo.
echo Your bot is now FREE FOREVER on Render!
echo.
pause
