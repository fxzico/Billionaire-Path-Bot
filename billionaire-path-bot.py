import os
import json
import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic
import schedule
import threading
import time

# Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
DATABASE_PATH = 'billionaire_path_data.db'

# Initialize database
def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Main entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            entry_type TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT
        )
    ''')

    # Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_text TEXT NOT NULL,
            target_year INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Affirmations library
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS affirmations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            affirmation_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Financial tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sip_amount REAL,
            investment_amount REAL,
            investment_type TEXT,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Database helper functions
def add_entry(user_id, entry_type, content, metadata=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO entries (user_id, entry_type, content, metadata) VALUES (?, ?, ?, ?)',
        (user_id, entry_type, content, json.dumps(metadata) if metadata else None)
    )
    conn.commit()
    conn.close()

def get_entries(user_id, entry_type=None, days=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    query = 'SELECT * FROM entries WHERE user_id = ?'
    params = [user_id]

    if entry_type:
        query += ' AND entry_type = ?'
        params.append(entry_type)

    if days:
        date_threshold = datetime.now() - timedelta(days=days)
        query += ' AND timestamp >= ?'
        params.append(date_threshold.strftime('%Y-%m-%d %H:%M:%S'))

    query += ' ORDER BY timestamp DESC'

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def add_goal(user_id, goal_text, target_year=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO goals (user_id, goal_text, target_year) VALUES (?, ?, ?)',
        (user_id, goal_text, target_year)
    )
    conn.commit()
    conn.close()

def add_affirmation(user_id, affirmation_text):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO affirmations (user_id, affirmation_text) VALUES (?, ?)',
        (user_id, affirmation_text)
    )
    conn.commit()
    conn.close()

def get_random_affirmation(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT affirmation_text FROM affirmations WHERE user_id = ? ORDER BY RANDOM() LIMIT 1',
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_finance_entry(user_id, sip_amount=None, investment_amount=None, investment_type=None, notes=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO finances (user_id, sip_amount, investment_amount, investment_type, notes) VALUES (?, ?, ?, ?, ?)',
        (user_id, sip_amount, investment_amount, investment_type, notes)
    )
    conn.commit()
    conn.close()

# Claude AI Analysis
def analyze_progress(user_id):
    # Gather all data
    all_entries = get_entries(user_id)
    recent_entries = get_entries(user_id, days=30)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,))
    goals = cursor.fetchall()

    cursor.execute('SELECT * FROM finances WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10', (user_id,))
    finances = cursor.fetchall()

    conn.close()

    # Prepare context for Claude
    context = f"""
You are analyzing Saptarshi's progress on the Billionaire Path. His ultimate vision:
- Build ₹10,000 Cr wealth
- Financial freedom by age 45
- Launch school in 2032 that creates 100 billionaires (who each create 1,000 millionaires)
- Platform to compound generational wealth starting from his hometown

Here's his tracking data:

GOALS:
{json.dumps([{'goal': g[2], 'target_year': g[3]} for g in goals], indent=2)}

RECENT ACTIVITY (Last 30 days):
Total entries: {len(recent_entries)}
- Wins logged: {len([e for e in recent_entries if e[3] == 'win'])}
- Good things logged: {len([e for e in recent_entries if e[3] == 'good_things'])}
- Progress updates: {len([e for e in recent_entries if e[3] == 'progress'])}
- Affirmation videos watched: {len([e for e in recent_entries if e[3] == 'affirmation_video'])}

RECENT ENTRIES:
{json.dumps([{'type': e[3], 'content': e[4][:100], 'date': e[2]} for e in recent_entries[:20]], indent=2)}

FINANCIAL PROGRESS:
{json.dumps([{'sip': f[3], 'investment': f[4], 'type': f[5], 'notes': f[6], 'date': f[2]} for f in finances], indent=2)}

OVERALL STATS:
- Total days tracked: {(datetime.now() - datetime.strptime(all_entries[-1][2], '%Y-%m-%d %H:%M:%S')).days if all_entries else 0}
- Total entries: {len(all_entries)}

Based on this data, provide:
1. Progress assessment: Is he on track toward ₹10,000 Cr and 2032 school goals?
2. Momentum analysis: Is activity increasing or decreasing?
3. Specific wins and patterns you notice
4. Reality check on financial trajectory (current SIP/investment pace vs ₹10,000 Cr target)
5. Actionable suggestions for the next 30 days
6. A motivational message scaled to his ambition (100 billionaires, not small goals)

Be honest and direct. He responds to ambition-scaled feedback, not "play it safe" advice.
Use his actual data points. If he's behind, say so and suggest course corrections.
"""

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": context}
        ]
    )

    return message.content[0].text

# Bot Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
💎 **Billionaire Path**

Track your journey to ₹10,000 Cr, financial freedom by 45, and the 2032 school that creates 100 billionaires.

**Commands:**

📝 **Daily Tracking:**
/win <text> - Log a daily win
/good <text> - Log 5 good things (separate with semicolons)
/progress <text> - Log any progress or new thing you did
/video <YT link> - Track affirmation video watched

💰 **Financial:**
/sip <amount> - Log SIP investment
/invest <amount> <type> <notes> - Log investment

🎯 **Goals & Affirmations:**
/goal <text> <year> - Add a goal with target year
/affirm - Get random affirmation from your library
/addaffirm <text> - Add affirmation to library

📊 **Analysis:**
/check - AI analysis of your progress toward ₹10,000 Cr
/stats - Quick stats overview

🗓️ **Travel & Life:**
/travel <location> <notes> - Log travel
/life <event> - Log major life event

Your second brain tracking inputs to billionaire-scale outcomes. Start with /win.
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def log_win(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    win_text = ' '.join(context.args)

    if not win_text:
        await update.message.reply_text("Usage: /win <your win text>")
        return

    add_entry(user_id, 'win', win_text)
    await update.message.reply_text(f"✅ Win logged. Momentum compounds.")

async def log_good_things(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    good_text = ' '.join(context.args)

    if not good_text:
        await update.message.reply_text("Usage: /good thing1; thing2; thing3; thing4; thing5")
        return

    add_entry(user_id, 'good_things', good_text)
    await update.message.reply_text(f"💚 5 good things logged. Gratitude compounds.")

async def log_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    progress_text = ' '.join(context.args)

    if not progress_text:
        await update.message.reply_text("Usage: /progress <what you accomplished>")
        return

    add_entry(user_id, 'progress', progress_text)
    await update.message.reply_text(f"🚀 Progress logged. Build daily.")

async def log_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    video_link = ' '.join(context.args)

    if not video_link:
        await update.message.reply_text("Usage: /video <YouTube link>")
        return

    add_entry(user_id, 'affirmation_video', video_link, {'link': video_link})
    await update.message.reply_text(f"🎥 Affirmation tracked. Mindset compounds.")

async def log_sip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /sip <amount>")
        return

    try:
        amount = float(context.args[0])
        add_finance_entry(user_id, sip_amount=amount)
        await update.message.reply_text(f"💰 SIP of ₹{amount:,.0f} logged. Wealth compounds.")
    except ValueError:
        await update.message.reply_text("Please provide a valid number.")

async def log_investment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /invest <amount> <type> <notes>")
        return

    try:
        amount = float(context.args[0])
        inv_type = context.args[1]
        notes = ' '.join(context.args[2:]) if len(context.args) > 2 else None

        add_finance_entry(user_id, investment_amount=amount, investment_type=inv_type, notes=notes)
        await update.message.reply_text(f"💎 ₹{amount:,.0f} in {inv_type} logged. Building the ₹10,000 Cr.")
    except ValueError:
        await update.message.reply_text("Please provide a valid amount.")

async def add_goal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /goal <goal text> <target year>")
        return

    try:
        target_year = int(context.args[-1])
        goal_text = ' '.join(context.args[:-1])
    except ValueError:
        target_year = None
        goal_text = ' '.join(context.args)

    add_goal(user_id, goal_text, target_year)
    await update.message.reply_text(f"🎯 Goal set: {goal_text}" + (f" by {target_year}" if target_year else ""))

async def get_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    affirmation = get_random_affirmation(user_id)

    if affirmation:
        await update.message.reply_text(f"✨ {affirmation}")
    else:
        await update.message.reply_text("No affirmations yet. Use /addaffirm to add some.")

async def add_affirmation_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    affirmation_text = ' '.join(context.args)

    if not affirmation_text:
        await update.message.reply_text("Usage: /addaffirm <your affirmation>")
        return

    add_affirmation(user_id, affirmation_text)
    await update.message.reply_text(f"✨ Affirmation added.")

async def check_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text("🤖 Analyzing your Billionaire Path progress... (~10 sec)")

    try:
        analysis = analyze_progress(user_id)
        await update.message.reply_text(analysis, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Analysis error: {str(e)}")

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    all_entries = get_entries(user_id)
    week_entries = get_entries(user_id, days=7)
    month_entries = get_entries(user_id, days=30)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM goals WHERE user_id = ?', (user_id,))
    goal_count = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(sip_amount), SUM(investment_amount) FROM finances WHERE user_id = ?', (user_id,))
    sip_total, inv_total = cursor.fetchone()
    conn.close()

    stats_text = f"""
📊 **Billionaire Path Stats**

**Overall:**
- Total entries: {len(all_entries)}
- Days tracked: {(datetime.now() - datetime.strptime(all_entries[-1][2], '%Y-%m-%d %H:%M:%S')).days if all_entries else 0}
- Goals set: {goal_count}

**Last 7 Days:**
- Total entries: {len(week_entries)}
- Wins: {len([e for e in week_entries if e[3] == 'win'])}
- Progress logs: {len([e for e in week_entries if e[3] == 'progress'])}

**Last 30 Days:**
- Total entries: {len(month_entries)}
- SIP invested: ₹{sip_total:,.0f if sip_total else 0}
- Other investments: ₹{inv_total:,.0f if inv_total else 0}

Use /check for AI analysis of your ₹10,000 Cr trajectory.
    """

    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def log_travel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("Usage: /travel <location> <notes>")
        return

    location = context.args[0]
    notes = ' '.join(context.args[1:]) if len(context.args) > 1 else None

    add_entry(user_id, 'travel', f"{location}: {notes}", {'location': location})
    await update.message.reply_text(f"✈️ Travel to {location} logged.")

async def log_life_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    event_text = ' '.join(context.args)

    if not event_text:
        await update.message.reply_text("Usage: /life <major event>")
        return

    add_entry(user_id, 'life_event', event_text)
    await update.message.reply_text(f"🌟 Life event logged.")

def main():
    init_database()
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("win", log_win))
    application.add_handler(CommandHandler("good", log_good_things))
    application.add_handler(CommandHandler("progress", log_progress))
    application.add_handler(CommandHandler("video", log_video))
    application.add_handler(CommandHandler("sip", log_sip))
    application.add_handler(CommandHandler("invest", log_investment))
    application.add_handler(CommandHandler("goal", add_goal_cmd))
    application.add_handler(CommandHandler("affirm", get_affirmation))
    application.add_handler(CommandHandler("addaffirm", add_affirmation_cmd))
    application.add_handler(CommandHandler("check", check_progress))
    application.add_handler(CommandHandler("stats", get_stats))
    application.add_handler(CommandHandler("travel", log_travel))
    application.add_handler(CommandHandler("life", log_life_event))

    # Run polling with drop_pending_updates to avoid conflicts
    print("Starting Billionaire Path Bot...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
    )

if __name__ == '__main__':
    main()
