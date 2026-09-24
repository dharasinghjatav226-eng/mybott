import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Mai ChatGPT jaisa bot hu, kuch bhi pucho!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
