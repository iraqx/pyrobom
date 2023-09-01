from telethon.sync import TelegramClient, events
import yt_dlp
import os

# Telegram API credentials
api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGZ4377Gvc7eqUY6xhT6bJfLozoyJNU8ME'  # Replace with your bot token

# Initialize the Telethon client
client = TelegramClient('bot_session', api_id, api_hash)

# Event handler for /start command
@client.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.reply("`Hi... `")

# Convert duration to readable format
def format_duration(duration):
    if duration < 60:
        return f"{duration} sec"
    elif duration < 3600:
        return f"{duration // 60} min"
    else:
        return f"{duration // 3600} hour"

# Event handler for incoming messages
@client.on(events.NewMessage)
async def process_video_link(event):
    message = event.message
    chat_id = message.chat_id
    text = message.text
    
    if text.startswith('https://'):
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        
        # Send a "Downloading..." message to the chat
        downloading_message = await client.send_message(chat_id, f"`Downloading...`")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(text, download=True)
            video_path = os.path.join('downloads', info_dict['title'] + '.' + info_dict['ext'])
            
            # Upload the video to the chat
            uploading_message = await client.send_file(chat_id, video_path, reply_to=downloading_message)
            await client.delete_messages(chat_id, [downloading_message.id])  # Delete the "Downloading..." message
            
            # Convert duration to readable format
            duration_formatted = format_duration(int(info_dict['duration']))
            
            # Update the message to display video information
            video_info = f"`Video Downloaded:\nTitle: {info_dict['title']}\nDuration: {duration_formatted}`"
            await client.edit_message(chat_id, uploading_message.id, video_info)
            
            # Remove the downloaded video from storage
            os.remove(video_path)
            

# Start the bot
client.start(bot_token=bot_token)
client.run_until_disconnected()
