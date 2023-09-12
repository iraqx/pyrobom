import os

from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
import concurrent.futures
import asyncio
from server import server
api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'
app = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.regex(r"(?i)^(https?://).+$"))
async def http_url_handler(client: Client, message: Message):
    url = message.text.strip()
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, download_video, url, message)
        
        
def download_video(url: str, message: Message):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(id)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            downloading_message = message.reply_text("`Downloading...`", quote=True)
            info = ydl.extract_info(url, download=True)
            video_id = info.get('id', None)
            if video_id:
                video_file = f"/sdcard/py/downloads/{video_id}.mp4"
                message.reply_video(video_file, quote=True)
                downloading_message.delete()
                
            else:
                downloading_message.delete()
                downloading_message.reply_text("`An error occurred while downloading the video.`")
        except Exception as e:
            error_message = f"`An error occurred: {str(e)}`"
            downloading_message.delete()
            message.reply_text(error_message, quote=True)

@app.on_message(filters.command("start"))
def start_command_handler(client, message):
    message.reply_text("`I am alive, send a link:`",quote=True)

@app.on_message(filters.command("help"))
def start_command_handler(client: Client, message: Message):
    message.reply_text("`Bro, just send a link 🗿`",quote=True)

@app.on_message(filters.command('sites'))
def help_command(client: Client, message: Message):
    message.reply_text(f"`Here is` [supported sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html)", disable_web_page_preview=True,quote=True)

@app.on_message(filters.regex(r".+"))
def unsupported_url_handler(client: Client, message: Message):
    message.reply_text("`This link is not supported.`",quote=True)
#try:
#	os.remove(tt)
#except:
#	u=1
#ttj="/sdcard/py/bot.session-journal"
#try:
#	os.remove(ttj)
#except:
#	e=1
server()
app.run()
