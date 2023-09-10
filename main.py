import os
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL

api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'
app = Client("uhhbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    message.reply_text("`send link`")

def download_video(url: str, message: Message):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': '%(id)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            downloading_message = message.reply_text("`Downloading...`")
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id', None)
            if video_id:
                video_file = f"{video_id}.mp4"
                
                message.reply_video(video_file)
                downloading_message.delete()
                os.remove(video_file)
            else:
                downloading_message.edit_text("`An error occurred while downloading the video.`")
        except Exception as e:
            # تجاهل الاستثناء واستمر في التنفيذ
            pass

@app.on_message(filters.regex(r"(?i)^(https?://).+$"))
def http_url_handler(client: Client, message: Message):
    url = message.text.strip()
    download_video(url, message)

@app.on_message(filters.regex(r".+"))
def unsupported_url_handler(client: Client, message: Message):
    message.reply_text("`link not support`")

app.run()
