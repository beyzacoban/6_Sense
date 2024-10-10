from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import requests  # Don't forget to import requests for sending the video to your server

# Replace with your bot token
BOT_TOKEN = "7163033954:AAHh936pvlv-7Hgk9U11HY1ARRJb5qvvoZY"  # Your actual token goes here
SERVER_URL = "http://yourserver.com/upload"  # Your server endpoint for video processing

async def open_camera(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please record a video and send it here.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the video file
    video_file = update.message.video.file_id
    new_file = await context.bot.get_file(video_file)

    # Download the video file
    video_path = f"video_{video_file}.mp4"
    await new_file.download(video_path)

    # Send the video to your server for processing
    await send_video_to_server(video_path)

    await update.message.reply_text("Video received and sent to the server for processing.")

async def send_video_to_server(video_path):
    # Open the video file and send it to your server
    with open(video_path, 'rb') as video_file:
        response = requests.post(SERVER_URL, files={'video': video_file})

    # Check response from the server
    if response.status_code == 200:
        print("Video processed successfully:", response.json())
    else:
        print("Failed to process video:", response.status_code)

def main():
    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("camera", open_camera))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))  # Corrected filter usage

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
