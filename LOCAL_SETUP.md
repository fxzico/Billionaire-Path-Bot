# Local Billionaire Path Bot - Quick Start

Run your bot **entirely on your PC**. No cloud, no deployment, no Railway.

## Setup (One Time - 2 Minutes)

### 1. Install Python (if you don't have it)
Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Open Command Prompt in this folder
- Press `Win + R`
- Type `cmd` and press Enter
- Type: `cd /d "G:\Claude\Manifestation Bot"`

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
- Open `.env` file in Notepad
- Replace `your_anthropic_api_key_here` with your real key from https://console.anthropic.com/settings/keys
- Save and close

## Run Your Bot (Every Time You Want to Use It)

### Option 1: Double-click
Just double-click `START_BOT.bat` in this folder.

### Option 2: Command line
```bash
python billionaire-path-bot.py
```

## How It Works

- **Bot runs only when your PC is on**
- All data saved to `G:\Claude\Manifestation Bot\data\`
- When PC is off, bot is off (Telegram messages wait for you)
- When you turn PC back on, run the bot again - all data is still there

## Auto-start on Boot (Optional)

If you want the bot to start automatically when you turn on your PC:

1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Copy `START_BOT.bat` into that folder
4. Done - bot starts with Windows

## Files

- `data/user_data.json` - Your manifestation entries
- `data/logs/` - Bot activity logs
- `.env` - Your API keys (never share this)

## Cost

₹8/month (Anthropic API only). No cloud hosting fees.

## Stop the Bot

Close the command window or press `Ctrl + C`

---

**Ready to start?** Double-click `START_BOT.bat` or follow Option 2 above.
