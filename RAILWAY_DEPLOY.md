# Railway One-Click Deploy Guide

Your bot is ready for Railway deployment.

## Option 1: One-Click Deploy (Easiest)

Click this button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/fxzico/Billionaire-Path-Bot)

**Or use this direct link:**
```
https://railway.app/new/template?template=https://github.com/fxzico/Billionaire-Path-Bot
```

### After Clicking:

1. Railway will ask you to login (use GitHub)
2. It will show your bot's name and ask for environment variables
3. Add these two variables:
   - `TELEGRAM_BOT_TOKEN` = `8634281755:AAEdhfrDSO1-amh0ws6OrKTsIp_i3R9C2aQ`
   - `ANTHROPIC_API_KEY` = `your_key_here` (get from https://console.anthropic.com/settings/keys)
4. Click "Deploy"
5. Done. Your bot will be live in 2 minutes.

## Option 2: Manual Railway Deploy

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose `fxzico/Billionaire-Path-Bot`
5. Add the environment variables above
6. Click "Deploy"

## Cost

Railway Free Tier: **$5 credit/month** (enough for your bot)

## After Deploy

Open Telegram → Search `@Zico_Billionaire_Path_bot` → `/start`

Your Billionaire Path tracking starts today.
