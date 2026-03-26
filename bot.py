import os
import requests
import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("TERABOX_API_KEY")

# ✅ তোমার Vercel player URL
PLAYER_URL = "https://final-terabox-bot.vercel.app/player.html"


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 Send Terabox link")


# ================= MAIN HANDLER =================
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("⏳ Processing...")

    try:
        api_url = "https://xapiverse.com/api/terabox-pro"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {"url": url}

        res = requests.post(api_url, json=payload, headers=headers, timeout=30)

        if res.status_code != 200:
            return await msg.edit_text("❌ API Error")

        data = res.json()

        if not data.get("success"):
            return await msg.edit_text("❌ Failed to fetch video")

        file = data["data"]

        download_url = file.get("download_url")
        file_name = file.get("file_name", "video.mp4")
        size = file.get("size", "Unknown")
        thumb = file.get("thumbnail")

        # ✅ PLAYER LINK (ENCODED)
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

        # ---------- TRY SEND VIDEO ----------
        try:
            if int(file.get("size_bytes", 0)) < 50 * 1024 * 1024:
                await update.message.reply_video(
                    video=download_url,
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return await msg.delete()
        except:
            pass

        # ---------- SEND WITH THUMB ----------
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


# ================= RUN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🚀 Bot Running...")

app.run_polling()
