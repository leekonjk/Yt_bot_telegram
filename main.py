from telegram import Update
from typing import Final
from pytube import YouTube
from telegram.ext import Application, CommandHandler, MessageHandler,ContextTypes,filters

TOKEN: Final = "Token"
BOT_USERNAME: Final = "Bot_Name"


# Function to sanitize a string to be used as a filename
def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove leading and trailing whitespaces
    filename = filename.strip()

    return filename

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Paste your Downloading Link")


async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    text = update.message.text
    try:
        yt = YouTube(text)
        stream = yt.streams.get_highest_resolution()
        sanitized_title = sanitize_filename(yt.title)
        stream.download()
        await update.message.reply_video(stream.download())
        await update.message.reply_text(f"Downloaded: {yt.title}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.Regex(r'^https?://.*'), download_command))
    app.run_polling(poll_interval=1)
    print("Bot is running...")