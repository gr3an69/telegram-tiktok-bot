import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" not in text:
        await update.message.reply_text("❌ Wyślij link do TikToka")
        return

    await update.message.reply_text("⏳ Pobieram wideo...")

    try:
        subprocess.run(
            ["yt-dlp", "-f", "mp4", "--no-playlist", "-o", "video.mp4", text],
            check=True
        )

        await update.message.reply_video(video=open("video.mp4", "rb"))
        os.remove("video.mp4")

    except Exception:
        await update.message.reply_text("❌ Błąd pobierania")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
