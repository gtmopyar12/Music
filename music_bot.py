import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from yt_dlp import YoutubeDL

# Define the download function
def download_music(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"{info['title']}.mp3"

# Define the start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a YouTube link, and I'll download the audio for you.")

# Handle YouTube link
def download(update: Update, context: CallbackContext):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        update.message.reply_text("Downloading the audio, please wait...")
        try:
            file_name = download_music(url)
            with open(file_name, 'rb') as audio:
                update.message.reply_audio(audio)
            os.remove(file_name)
        except Exception as e:
            update.message.reply_text(f"An error occurred: {e}")
    else:
        update.message.reply_text("Please send a valid YouTube link.")

# Main function to run the bot
def main():
    TOKEN = "8160773777:AAHatjplSQ9WhKYUnS_oNUd5Z-4CfRRwbjY"  # Replace with your bot's API token
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("download", download))
    dp.add_handler(CommandHandler(None, download))  # Catch YouTube links

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()