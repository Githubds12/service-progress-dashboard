import os
import re
import logging
import asyncio
import datetime
import subprocess
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
from PIL import Image
import json

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
REPORTS_DIR = os.getenv("REPORTS_DIR", r"c:\Users\Gorri\Documents\Reports")
TIME_LOG_FILE = os.path.join(REPORTS_DIR, "trackers", "Time Log.txt")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Gemini
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-flash-latest') # Fallback to flash-latest

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Project Pulse Report Bot!\n\n"
        "Send me a screenshot of an App's Info page or an SMS, and I'll extract the text and key details for your report.\n\n"
        "Please ensure you have set `GEMINI_API_KEY` in your `.env` file."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not GEMINI_KEY:
        await update.message.reply_text("❌ GEMINI_API_KEY is missing in .env. Please add it to enable OCR.")
        return

    # Get the highest resolution photo
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    # Save file temporarily with unique ID
    msg_id = update.message.message_id
    temp_path = f"temp_ss_{msg_id}.jpg"
    await file.download_to_drive(temp_path)
    
    await update.message.reply_text("🔍 Analyzing image with Gemini AI... please wait.")
    
    try:
        # Load image for Gemini (using context manager to ensure it closes)
        with Image.open(temp_path) as img:
            # Define the prompt
            prompt = """
            Analyze this screenshot. It is either an Android App Info page or an SMS message.
            1. Extract all visible text.
            2. Identify the App Name, Package Name, and Version if present.
            3. Identify any OTP (One-Time Password) if this is an SMS.
            4. Return the data in a clear format.
            """
            
            # Retry logic for 429
            max_retries = 3
            analysis_text = ""
            for attempt in range(max_retries):
                try:
                    response = model.generate_content([prompt, img])
                    analysis_text = response.text
                    break
                except Exception as e:
                    logging.error(f"Gemini Error (Attempt {attempt+1}): {e}")
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)
                        logging.warning(f"Quota hit, retrying in {wait_time}s...")
                        await update.message.reply_text(f"⏳ Quota reached, retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        raise e
            
            logging.info(f"Gemini Analysis Result: {analysis_text}")
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        await update.message.reply_text(f"✅ **Analysis Result:**\n\n{analysis_text}", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        await update.message.reply_text(f"❌ Error processing image: {str(e)}")

async def log_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/log [Activity] [Hours]h [Note]`\nExample: `/log Coding 2h Fixed chart bug`", parse_mode='Markdown')
        return

    raw_args = " ".join(context.args)
    match = re.search(r'^(.*?)\s+(\d+\.?\d*)h(?:\s+(.*))?$', raw_args)
    
    if not match:
        await update.message.reply_text("❌ Invalid format. Use `[Activity] [Hours]h [Note]`", parse_mode='Markdown')
        return

    activity, hours, note = match.groups()
    today_str = datetime.now().strftime("%A, %d-%m-%Y")
    entry = f"- {activity.strip()}: {hours}h"
    if note: entry += f" ({note.strip()})"
    
    try:
        content = ""
        if os.path.exists(TIME_LOG_FILE):
            with open(TIME_LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
        
        date_header = f"Date: {today_str}"
        if date_header in content:
            parts = content.split(date_header)
            subparts = parts[1].split('Date:', 1)
            new_section = subparts[0].strip() + "\n" + entry
            content = parts[0] + date_header + "\n" + new_section + ("\nDate:" + subparts[1] if len(subparts) > 1 else "")
        else:
            header_end = content.find('\n\n') + 2 if '\n\n' in content else 0
            new_section = f"\nDate: {today_str}\n{entry}\nPerformance Note: First entry for today.\n"
            content = content[:header_end] + new_section + content[header_end:]

        with open(TIME_LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
            
        await update.message.reply_text(f"✅ **Time Logged!**\nActivity: {activity}\nHours: {hours}h\n\nDashboard is updating...", parse_mode='Markdown')
        subprocess.Popen([r".venv\Scripts\python", "scripts/update_dashboard.py"])
    except Exception as e:
        await update.message.reply_text(f"❌ Error logging time: {str(e)}")

async def get_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_path = os.path.join(REPORTS_DIR, "dashboard_data.js")
    if not os.path.exists(data_path):
        await update.message.reply_text("❌ Dashboard data not found. Run /sync first.")
        return

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract JSON from "window.dashboardData = {...};"
            json_str = content.split('window.dashboardData = ', 1)[1].rsplit(';', 1)[0]
            data = json.loads(json_str)
            stats = data['stats']
            
            msg = (
                f"📊 **CyberCore Dashboard Stats**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💰 **Total Earned:** ₹{stats['total_earnings']}\n"
                f"🛠 **Total Services:** {stats['total_services']}\n"
                f"📈 **Daily Average:** ₹{stats['avg_daily']}/day\n"
                f"🎯 **Today's Goal:** {stats['completed_today']}/{stats['recommended_today']}\n"
                f"⏳ **Recovery Pace:** {stats['recovery_pace_services']} services/day\n"
                f"🔮 **Monthly Proj:** ₹{stats['projected_total']}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📝 *{stats['explanation']}*"
            )
            await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching stats: {str(e)}")

async def sync_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Syncing dashboard and GitHub... please wait.")
    try:
        # Run the update script and wait for it
        process = subprocess.run([r".venv\Scripts\python", "scripts/update_dashboard.py"], capture_output=True, text=True)
        if process.returncode == 0:
            await update.message.reply_text("✅ **Sync Complete!** GitHub and Dashboard are now up to date.", parse_mode='Markdown')
            # Follow up with stats
            await get_stats(update, context)
        else:
            await update.message.reply_text(f"❌ **Sync Failed!**\nError: {process.stderr[:200]}", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Error triggering sync: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("log", log_time))
    application.add_handler(CommandHandler("stats", get_stats))
    application.add_handler(CommandHandler("sync", sync_dashboard))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_photo))
    
    print("Bot is starting...")
    application.run_polling()
