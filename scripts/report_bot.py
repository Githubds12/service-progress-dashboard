import os
import re
import logging
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv
from PIL import Image
import json

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
REPORTS_DIR = os.getenv("REPORTS_DIR", r"c:\Users\Gorri\Documents\Reports")

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Gemini
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-flash-latest') # Using the latest stable flash model

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
    
    # Save file temporarily
    temp_path = "temp_screenshot.jpg"
    await file.download_to_drive(temp_path)
    
    await update.message.reply_text("🔍 Analyzing image with Gemini AI... please wait.")
    
    try:
        # Load image for Gemini
        img = Image.open(temp_path)
        
        # Define the prompt
        prompt = """
        Analyze this screenshot. It is either an Android App Info page or an SMS message.
        1. Extract all visible text.
        2. Identify the App Name, Package Name, and Version if present.
        3. Identify any OTP (One-Time Password) if this is an SMS.
        4. Return the data in a clear format.
        """
        
        # Generate content
        response = model.generate_content([prompt, img])
        analysis_text = response.text
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        await update.message.reply_text(f"✅ **Analysis Result:**\n\n{analysis_text}", parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        await update.message.reply_text(f"❌ Error processing image: {str(e)}")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot is starting...")
    application.run_polling()
