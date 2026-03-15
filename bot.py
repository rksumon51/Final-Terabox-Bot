import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_KEY = os.getenv("RAPID_API_KEY")
API_HOST = "terabox-downloader-online-viewer-player-api.p.rapidapi.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send Terabox link")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("⏳ Processing...")

    try:

        endpoint = "https://terabox-downloader-online-viewer-player-api.p.rapidapi.com/api/downloader"

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }

        params = {
            "url": url
        }

        r = requests.get(endpoint, headers=headers, params=params)

        data = r.json()

        if data["status"] == "success":

            video = data["data"]["download_url"]

            await update.message.reply_video(video)

        else:

            await update.message.reply_text("❌ Failed to fetch video")

    except Exception as e:

        await update.message.reply_text(f"❌ Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Running")

app.run_polling()
