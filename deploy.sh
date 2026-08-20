#!/bin/bash
# One-click deployment script for Railway

echo "🚀 Billionaire Path Bot - Railway Deployment"
echo "=============================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please add your Anthropic API key to .env first"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if grep -q "your_anthropic_api_key_here" .env; then
    echo "❌ Error: Please set your ANTHROPIC_API_KEY in .env"
    echo "Get it from: https://console.anthropic.com/settings/keys"
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Create new project
echo "📁 Creating Railway project..."
railway init

# Set environment variables from .env
echo "⚙️  Setting environment variables..."
railway variables --from-file .env

# Deploy
echo "🚀 Deploying bot..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your bot is live at: t.me/Zico_Billionaire_Path_bot"
echo ""
echo "Next steps:"
echo "1. Open Telegram and start a chat with your bot"
echo "2. Send /start to initialize"
echo "3. Log your first entry with /log"
echo ""
echo "Monitor logs: railway logs"
echo "Check status: railway status"
