from telethon.sync import TelegramClient, events
import yt_dlp
import os

api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'

client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.reply("`🗿 `")

# Event handler for incoming messages
@client.on(events.NewMessage)
async def process_video_link(event):
    message = event.message
    chat_id = message.chat_id
    text = message.text

    if text.startswith('https://'):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Get the best quality video
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save with ID as filename
        }

        # Send an initial "Downloading..." message to the chat
        downloading_message = await client.send_message(chat_id, f"`Downloading...`")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(text, download=True)
            video_path = os.path.join('downloads', info_dict['id'] + '.' + info_dict['ext'])

            # Replace the "Downloading..." message with "Uploading..."
            uploading_message = await client.edit_message(chat_id, downloading_message.id, f"`Uploading...`")

            # Upload the video to the chat
            video = await client.upload_file(video_path, file_name=video_path)
            await client.send_file(chat_id, file=video, reply_to=downloading_message)

            # Remove the uploaded video from storage
            os.remove(video_path)

            # Delete the "Uploading..." message
            await client.delete_messages(chat_id, [uploading_message.id])
    else:
        await client.send_message(chat_id, f"`Please send a valid link`")

client.start(bot_token=bot_token)
client.run_until_disconnected()
