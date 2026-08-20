# Quick Start Guide - Billionaire Path Bot

## 1. Get Your API Keys

### Telegram Bot Token
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Name it: "Billionaire Path" (or your preference)
5. Username: `yourname_billionaire_bot` (must end in `_bot`)
6. **Copy the token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Anthropic API Key
1. Go to https://console.anthropic.com
2. Sign up (free, just email)
3. Click "API Keys" → "Create Key"
4. **Copy the key** (starts with: `sk-ant-`)
5. Add $10-20 credit (Settings → Billing)
   - Each AI analysis costs ~₹0.80
   - $10 = ~150 analyses (5+ months daily checks)

---

## 2. Deploy to Railway (Free - Recommended)

### Why Railway?
- Free 500 hours/month (24/7 uptime)
- No credit card required
- Auto-deploys on code push
- Runs even when your PC is off

### Steps:

**A. Create GitHub Repo**
1. Go to https://github.com/new
2. Name it: `billionaire-path-bot`
3. Make it **Private**
4. Create repo
5. Upload these files:
   - `billionaire-path-bot.py`
   - `requirements.txt`
   - `README.md`
   - `QUICK_START.md`

**B. Deploy on Railway**
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `billionaire-path-bot` repo
6. Railway auto-detects Python and installs dependencies

**C. Add Environment Variables**
1. Click on your deployed service
2. Go to "Variables" tab
3. Click "New Variable"
4. Add:
   ```
   TELEGRAM_BOT_TOKEN = (paste your token from BotFather)
   ANTHROPIC_API_KEY = (paste your key from Anthropic)
   ```
5. Bot auto-deploys

**D. Verify It's Running**
1. Click "Deployments" tab
2. Wait for "Success" (~1 minute)
3. Click "View Logs"
4. Should see: Bot started successfully

---

## 3. Start Using Your Bot

1. Open Telegram
2. Search for your bot username
3. Click "Start" or send `/start`
4. Welcome message appears with commands

### First Time Setup

**Set your goals:**
```
/goal Build ₹10,000 Cr wealth 2045
/goal Launch school that creates 100 billionaires 2032
/goal Financial freedom by 45 2032
```

**Add affirmations:**
```
/addaffirm I am building ₹10,000 Cr from my hometown
/addaffirm I create 100 billionaires who create 1,000 millionaires each
/addaffirm Wealth compounds through me
/addaffirm I work for passion, not money, after 45
```

**Log current financial state:**
```
/sip 10000
/invest 50000 mutual-funds Started equity investing
```

---

## 4. Daily Usage (2 Minutes)

**Morning:**
```
/video https://youtube.com/watch?v=xyz
```

**Evening:**
```
/win Closed new F&B client for ₹2L project
/good Morning walk; Productive client call; Read 20 pages; Hit gym; Made progress on automation
/progress Learned Telegram Bot API and deployed Billionaire Path bot
```

**Weekly (Sunday morning):**
```
/check
```
Wait 10 seconds for AI analysis

---

## 5. Alternative: Run Locally (Quick Test)

**Windows:**
```bash
pip install -r requirements.txt
set TELEGRAM_BOT_TOKEN=your_token_here
set ANTHROPIC_API_KEY=your_key_here
python billionaire-path-bot.py
```

**Mac/Linux:**
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=your_token_here
export ANTHROPIC_API_KEY=your_key_here
python billionaire-path-bot.py
```

Bot runs while terminal is open. Close = bot stops.

---

## 6. Commands Cheat Sheet

```
📝 DAILY TRACKING
/win <text> - Log a win
/good <5 things> - Log good things (separate with ;)
/progress <text> - Log progress or learning
/video <link> - Track affirmation video

💰 FINANCIAL
/sip <amount> - Log monthly SIP
/invest <amount> <type> <notes> - Log investment

🎯 GOALS & AFFIRMATIONS
/goal <text> <year> - Add goal
/affirm - Get random affirmation
/addaffirm <text> - Add to library

📊 ANALYSIS
/check - Full AI analysis (~10 sec)
/stats - Quick stats

🌍 LIFE LOGGING
/travel <location> <notes>
/life <event>
```

---

## 7. What AI Analysis Tells You

When you run `/check`, Claude analyzes:

✅ **Progress toward ₹10,000 Cr** - On track / behind / ahead
✅ **2032 school timeline** - Realistic or need acceleration
✅ **Financial trajectory** - Current SIP pace vs target wealth
✅ **Momentum** - Activity building, flat, or declining
✅ **Patterns** - What's working, what dropped off
✅ **Reality check** - Honest assessment, not generic motivation
✅ **Next 30 days** - Specific actions to course-correct

---

## 8. Cost Breakdown

- **Telegram:** Free forever
- **Railway hosting:** Free (500 hrs/month)
- **GitHub private repo:** Free
- **Anthropic API:** ~₹8/month (daily `/check`)

**Total: ₹8/month** for AI tracking toward ₹10,000 Cr.

---

## 9. Troubleshooting

**Bot doesn't respond:**
- Check Railway logs for errors
- Verify environment variables set correctly
- Make sure you clicked "Start" in Telegram

**AI analysis fails:**
- Check Anthropic API key is valid
- Verify you have credits ($10+ recommended)
- Look at Railway logs for error details

**Want to update code:**
- Edit file in GitHub repo
- Railway auto-deploys on commit
- Check logs to verify deployment

---

## 10. Daily Habit Setup

Set phone reminders:
- **9 PM:** Log wins + good things + progress
- **Morning (if watching video):** `/video <link>`
- **Sunday 9 AM:** Run `/check`

The bot only works if you feed it consistently.

Aim for **3-5 entries per week minimum**.

---

## 11. Backup Your Data

Railway stores `billionaire_path_data.db`.

To backup:
1. Railway dashboard → service → "Data" tab
2. Download `billionaire_path_data.db`
3. Save to your credentials Google Drive

Do this monthly.

---

## Why This Matters

You have a specific vision:
- ₹10,000 Cr wealth
- 100 billionaires from your 2032 school
- Financial freedom by 45

Six years to 2032. 19 years to 45.

Most people set goals and forget them. You'll have AI telling you weekly if you're on pace.

Log 3 entries per week = **936 data points by 2032**. The AI will see patterns you miss.

That's the edge.

---

**Deploy it today. Start logging tonight.**

Full details in `README.md`.
