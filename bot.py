import os
import requests
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

PLAYER_URL = "https://final-terabox-bot.vercel.app/player.html"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send Terabox link")


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    msg = await update.message.reply_text("⏳ Processing...")

    try:
        api_url = f"https://terabox-downloader-api.vercel.app/api?url={url}"

        res = requests.get(api_url, timeout=30)

        if res.status_code != 200:
            return await msg.edit_text(f"❌ API Error\n{res.text}")

        data = res.json()

        if not data.get("success"):
            return await msg.edit_text("❌ Failed")

        file = data["data"]

        download_url = file.get("download")
        file_name = file.get("filename", "video.mp4")
        size = file.get("size", "Unknown")
        thumb = file.get("thumbnail")

        encoded = urllib.parse.quote(download_url, safe="")
        player_link = f"{PLAYER_URL}?url={encoded}"

        buttons = [
            [InlineKeyboardButton("⬇️ Download", url=download_url)],
            [InlineKeyboardButton("🎬 Watch Online", url=player_link)]
        ]

        caption = f"""✅ Completed

🎬 Title: {file_name}
📦 Size: {size}
"""

        if thumb:
            await update.message.reply_photo(
                photo=thumb,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await msg.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🚀 Bot Running...")

app.run_polling()
