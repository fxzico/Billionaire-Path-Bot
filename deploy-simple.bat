@echo off
echo.
echo ========================================
echo   SUPER SIMPLE RENDER DEPLOYMENT
echo   No GitHub CLI Needed
echo ========================================
echo.

REM Step 1: Initialize Git
if not exist ".git\" (
    echo [Step 1/5] Setting up Git...
    git init
    git add .
    git commit -m "Billionaire Path Bot - Initial commit"
    echo ✅ Git ready
) else (
    echo [Step 1/5] Git already initialized
    git add .
    git commit -m "Update for Render deployment" 2>nul
)

echo.
echo [Step 2/5] Opening GitHub to create repository...
echo.
start https://github.com/new
echo.
echo ========================================
echo   IN THE GITHUB PAGE THAT JUST OPENED:
echo ========================================
echo.
echo 1. Repository name: Billionaire-Path-Bot
echo 2. Make it PUBLIC
echo 3. Do NOT add README, gitignore, or license
echo 4. Click "Create repository"
echo.
echo Then come back here and press any key...
pause >nul

echo.
echo [Step 3/5] Enter your GitHub username:
set /p GITHUB_USER="Username: "

echo.
echo [Step 4/5] Connecting to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/Billionaire-Path-Bot.git
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ⚠️  Git push failed. You may need to authenticate.
    echo.
    echo Run this command and follow the prompts:
    echo   git push -u origin main
    echo.
    echo Then continue with Step 5 below.
    pause
) else (
    echo ✅ Code pushed to GitHub
)

echo.
echo [Step 5/5] Opening Render dashboard...
start https://dashboard.render.com/select-repo?type=web

echo.
echo ========================================
echo   IN THE RENDER PAGE THAT JUST OPENED:
echo ========================================
echo.
echo 1. Click "Connect Repository" button
echo 2. Find "Billionaire-Path-Bot" in the list
echo 3. Click "Connect"
echo.
echo 4. Render will auto-configure from render.yaml
echo.
echo 5. Scroll to "Environment Variables"
echo 6. Click "Add Environment Variable" (twice)
echo.
echo    Variable 1:
echo    Key: TELEGRAM_BOT_TOKEN
echo    Value: [Get from .env file in your project folder]
echo.
echo    Variable 2:
echo    Key: ANTHROPIC_API_KEY
echo    Value: [Get from .env file in your project folder]
echo.
echo 7. Click "Create Web Service"
echo.
echo 8. Wait 3-5 minutes for build to complete
echo.
echo ========================================
echo   AFTER DEPLOYMENT COMPLETES:
echo ========================================
echo.
echo Open Telegram and search: @Zico_Billionaire_Path_bot
echo Send: /start
echo Send: /log Today I deployed my bot. First step to 10000 Cr.
echo.
echo Your bot is now FREE FOREVER!
echo.
pause
