@echo off
REM One-click deployment script for Railway (Windows)

echo 🚀 Billionaire Path Bot - Railway Deployment
echo ==============================================
echo.

REM Check if Railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Railway CLI...
    npm install -g @railway/cli
)

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please add your Anthropic API key to .env first
    exit /b 1
)

REM Check if ANTHROPIC_API_KEY is set
findstr /C:"your_anthropic_api_key_here" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo ❌ Error: Please set your ANTHROPIC_API_KEY in .env
    echo Get it from: https://console.anthropic.com/settings/keys
    exit /b 1
)

echo ✅ Environment configured
echo.

REM Login to Railway
echo 🔐 Logging into Railway...
railway login

REM Create new project
echo 📁 Creating Railway project...
railway init

REM Deploy
echo 🚀 Deploying bot...
railway up

echo.
echo ✅ Deployment complete!
echo.
echo Your bot is live at: t.me/Zico_Billionaire_Path_bot
echo.
echo Next steps:
echo 1. Open Telegram and start a chat with your bot
echo 2. Send /start to initialize
echo 3. Log your first entry with /log
echo.
echo Monitor logs: railway logs
echo Check status: railway status
