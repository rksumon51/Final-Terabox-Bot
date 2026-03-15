import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = "https://api-production-359d.up.railway.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send Terabox link")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    msg = await update.message.reply_text("⏳ Processing...")

    try:

        r = requests.post(f"{API}/generate_file", json={"url": url})
        data = r.json()

        file = data["list"][0]

        payload = {
            "shareid": data["shareid"],
            "uk": data["uk"],
            "sign": data["sign"],
            "timestamp": data["timestamp"],
            "fs_id": file["fs_id"]
        }

        r2 = requests.post(f"{API}/generate_link", json=payload)
        link_data = r2.json()

        video = link_data["download_link"]

        webplayer = f"https://yourdomain.vercel.app/player.html?url={video}"

        buttons = [
            [InlineKeyboardButton("▶️ Watch Online", url=webplayer)],
            [InlineKeyboardButton("⬇️ Download", url=video)]
        ]

        await msg.edit_text(
            "✅ Video Ready",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("Bot Running")

app.run_polling()
