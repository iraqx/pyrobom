from telethon.sync import TelegramClient, events
import yt_dlp
import os
import asyncio

api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'  # يمكنك تغييره إلى التوكن الذي تريده

client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage)
async def process_messages(event):
    message = event.message
    chat_id = message.chat_id
    text = message.text

    if text == '/start':
        await event.reply("`send link `")
    elif text.startswith('https://'):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Get the best quality MP4 video
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save with ID as filename
        }

        # Send an initial "Downloading..." message to the chat
        downloading_message = await client.send_message(chat_id, f"`Downloading...`")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(text, download=True)
                video_path = os.path.join('downloads', info_dict['id'] + '.' + 'mp4')
            except Exception as e:
                # If there's an error in downloading, try with the best quality
                ydl_opts['format'] = 'best'
                info_dict = ydl.extract_info(text, download=True)
                video_path = os.path.join('downloads', info_dict['id'] + '_best' + '.' + 'mp4')

            # Send the video to the chat
            await client.send_file(
                chat_id,
                video_path,
                reply_to=downloading_message
            )

            # Remove the uploaded video from storage
            os.remove(video_path)

            # Delete the "Downloading..." message
            await client.delete_messages(chat_id, [downloading_message.id])
    elif not text.startswith('https://'):
        await client.send_message(chat_id, f"`invalid link`")

client.start(bot_token=bot_token)
client.run_until_disconnected()
