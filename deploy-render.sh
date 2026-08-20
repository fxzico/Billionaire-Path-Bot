#!/bin/bash
set -e

echo "🚀 Deploying Billionaire Path Bot to Render..."
echo ""

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "📦 Installing Render CLI..."
    npm install -g @render/cli
fi

# Login to Render
echo "🔐 Logging into Render..."
echo "A browser window will open. Log in with your account."
render login

# Create the service
echo ""
echo "🔨 Creating service on Render..."
render services create --from-yaml render.yaml

echo ""
echo "✅ Service created! Now setting environment variables..."

# Get service ID (you'll need to set this manually after first creation)
echo ""
echo "⚙️  Setting environment variables..."
echo ""
echo "Please run these commands to set your secrets:"
echo ""
echo "render env set TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN"
echo "render env set ANTHROPIC_API_KEY=YOUR_ANTHROPIC_KEY"
echo ""
echo "Then deploy with: render deploy"
echo ""
echo "🎉 Almost done!"
