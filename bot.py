import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

API_URL = "https://terabox-downloader-online-viewer-player-api.p.rapidapi.com/api/downloader"

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "terabox-downloader-online-viewer-player-api.p.rapidapi.com"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send Terabox link")


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("⏳ Processing...")

    try:

        params = {"url": url}

        r = requests.get(API_URL, headers=headers, params=params)
        data = r.json()

        if "data" not in data:
            await update.message.reply_text("❌ Failed to fetch video")
            return

        video = data["data"]["download_url"]

        await update.message.reply_video(video)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

app.add_error_handler(error_handler)

print("Bot Running")

app.run_polling()
