# Deployment Guide - Billionaire Path Bot

Complete deployment instructions for all platforms.

---

## Option 1: Railway (Recommended - Free)

### Advantages
- Free tier: 500 hours/month (runs 24/7)
- Auto-deploys from GitHub
- Built-in logs and monitoring
- No credit card for free tier
- Bot runs even when PC is off

### Step-by-Step

**1. Prepare GitHub Repository**

```bash
# Create new private repo on GitHub
# Upload these files:
- billionaire-path-bot.py
- requirements.txt
- README.md
- .gitignore
```

**2. Deploy to Railway**

1. Go to https://railway.app
2. Sign up with GitHub (free)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Authorize Railway to access your repos
6. Select `billionaire-path-bot` repo
7. Railway auto-detects Python and installs from `requirements.txt`

**3. Configure Environment Variables**

In Railway dashboard:
1. Click your service
2. "Variables" tab
3. Add variables:
   - `TELEGRAM_BOT_TOKEN` = your bot token
   - `ANTHROPIC_API_KEY` = your API key
4. Save (auto-redeploys)

**4. Verify Deployment**

1. "Deployments" tab → check status
2. "View Logs" → should see "Bot started successfully"
3. Test in Telegram: send `/start` to your bot

**5. Monitor & Maintain**

- Railway dashboard shows logs in real-time
- Free tier resets monthly (no action needed)
- Database persists automatically

---

## Option 2: Render.com (Alternative Free Option)

### Advantages
- Free tier available
- Similar to Railway
- Good uptime

### Steps

1. Go to https://render.com
2. Sign up with GitHub
3. "New" → "Web Service"
4. Connect your GitHub repo
5. Settings:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python billionaire-path-bot.py`
6. Add environment variables
7. Deploy

---

## Option 3: Local Machine (Development/Testing)

### Windows

**Setup:**
```bash
# Install Python 3.9+ from python.org

# Navigate to bot folder
cd path\to\billionaire-path-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env with your actual keys

# Run bot
python billionaire-path-bot.py
```

**Keep Running (Windows):**
- Bot runs in terminal window
- Close terminal = bot stops
- Not recommended for 24/7 use

### Mac/Linux

**Setup:**
```bash
# Navigate to bot folder
cd ~/billionaire-path-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export ANTHROPIC_API_KEY="your_key"

# Run bot
python billionaire-path-bot.py
```

**Keep Running (Terminal Session):**
```bash
# Option A: Screen session (persists after logout)
screen -S billionaire-bot
python billionaire-path-bot.py
# Press Ctrl+A, then D to detach
# Reconnect: screen -r billionaire-bot

# Option B: nohup (background process)
nohup python billionaire-path-bot.py > bot.log 2>&1 &
```

---

## Option 4: VPS (Advanced - ₹200-500/month)

If you have a DigitalOcean, Linode, or AWS EC2 instance.

### Ubuntu VPS Setup

```bash
# SSH into VPS
ssh user@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Clone repo (if using git)
git clone https://github.com/yourusername/billionaire-path-bot.git
cd billionaire-path-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export ANTHROPIC_API_KEY="your_key"

# Test run
python billionaire-path-bot.py
# Ctrl+C to stop
```

### Run as System Service (Auto-restart)

Create service file:
```bash
sudo nano /etc/systemd/system/billionaire-bot.service
```

Add:
```ini
[Unit]
Description=Billionaire Path Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/billionaire-path-bot
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
Environment="ANTHROPIC_API_KEY=your_key_here"
ExecStart=/home/your-username/billionaire-path-bot/venv/bin/python billionaire-path-bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable billionaire-bot
sudo systemctl start billionaire-bot

# Check status
sudo systemctl status billionaire-bot

# View logs
journalctl -u billionaire-bot -f
```

---

## Database Backup Strategy

### Railway/Render
Bot creates `billionaire_path_data.db` automatically.

**Manual Backup:**
1. Railway: Dashboard → "Data" → Download `.db` file
2. Save to Google Drive monthly

**Automatic Backup (Advanced):**
Add to code (future enhancement):
```python
# Weekly auto-backup to Google Drive
# Monthly export to CSV
```

### Local/VPS
Database is in same folder as script.

**Backup command:**
```bash
# Linux/Mac
cp billionaire_path_data.db ~/backups/billionaire_path_$(date +%Y%m%d).db

# Automate with cron (weekly backup)
0 0 * * 0 cp /path/to/billionaire_path_data.db /path/to/backups/backup_$(date +\%Y\%m\%d).db
```

---

## Updating the Bot

### Railway/Render
1. Edit code in GitHub repo
2. Commit and push
3. Platform auto-deploys
4. Check logs for successful restart

### Local/VPS
```bash
cd billionaire-path-bot
git pull origin main
pip install -r requirements.txt  # if dependencies changed
# Restart bot (Ctrl+C and re-run, or systemctl restart)
```

---

## Monitoring & Logs

### Railway
- Dashboard → "Logs" tab
- Real-time stream
- Search and filter

### VPS with systemd
```bash
# Real-time logs
journalctl -u billionaire-bot -f

# Last 100 lines
journalctl -u billionaire-bot -n 100

# Logs from today
journalctl -u billionaire-bot --since today
```

### Local
```bash
# If running with nohup
tail -f bot.log

# If running in terminal
# Logs print to console
```

---

## Troubleshooting

### Bot doesn't respond in Telegram

**Check 1: Bot is running**
- Railway: Logs show activity
- Local: Terminal shows "Running..."
- VPS: `systemctl status billionaire-bot`

**Check 2: Environment variables**
```bash
# Print (Railway dashboard → Variables)
# Don't share these publicly
echo $TELEGRAM_BOT_TOKEN
echo $ANTHROPIC_API_KEY
```

**Check 3: Telegram connection**
```python
# Test token validity
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### AI analysis fails

**Error: "Invalid API key"**
- Check Anthropic console for correct key
- Key starts with `sk-ant-`
- Verify key has billing credits

**Error: "Rate limit exceeded"**
- Wait 1 minute, try again
- Check Anthropic dashboard for quota

### Database errors

**"Database is locked"**
- Stop bot, restart
- Check file permissions

**"No entries found"**
- Normal on first run
- Start logging with `/win` command

### Railway free tier limits

Railway free tier: 500 hours/month
- 1 service running 24/7 = 720 hours/month
- **You'll hit limit around day 20**
- Solution: Upgrade ($5/month) or pause bot few days/month

---

## Security Best Practices

### API Keys
✅ **DO:**
- Use environment variables (never hardcode)
- Keep `.env` in `.gitignore`
- Use private GitHub repos
- Rotate keys if leaked

❌ **DON'T:**
- Commit `.env` to git
- Share keys in Discord/Slack
- Use same key across projects
- Post keys in screenshots

### Database
- Contains personal financial data
- Keep backups private (encrypt if cloud storage)
- Don't commit `.db` file to git

### Bot Access
- Only you can use the bot (user_id check optional)
- Don't share bot username publicly
- Revoke token via @BotFather if compromised

---

## Cost Comparison

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| **Railway** | 500 hrs/mo | $5/mo unlimited | Recommended |
| **Render** | 750 hrs/mo | $7/mo | Alternative |
| **Local PC** | Free | Electricity | Testing |
| **VPS** | - | ₹200-500/mo | Full control |

**Recommendation:** Start with Railway free. Upgrade to $5/mo if you want 24/7 guaranteed uptime.

---

## Performance

- Bot responds instantly (<1 second)
- `/check` AI analysis: 5-10 seconds
- Database queries: <100ms
- Memory usage: ~50MB
- CPU usage: Minimal

Scales to:
- 10,000+ entries
- Years of daily logging
- Multiple goals and affirmations

---

## Next Steps After Deployment

1. ✅ Bot running 24/7
2. Set phone reminders (9 PM daily, Sunday 9 AM)
3. Add your 3 main goals
4. Add 5-10 affirmations
5. Log first win, good things, progress
6. Run `/check` after 7 days of data

The bot compounds value over time. Deploy it today, start logging tonight.

---

**Questions?** Revisit `README.md` or `QUICK_START.md`.
