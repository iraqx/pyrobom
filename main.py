# bot.py

import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

api_id = 27495900
api_hash = 'f5e05aadcfca1c374b55fdad2fe2029e'
bot_token = '6460565675:AAHSlI5R6SLwy9qjjxNgfNLTaK1opaY--1I'

app = Client("video_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("video"))
async def video_handler(_, message):

  try:
    url = message.text.split(None, 1)[1]
  except IndexError:
    await message.reply("Please provide a URL to download.")
    return

  await message.reply("`Downloading...`")

  ydl_opts = {"outtmpl": "%(id)s.mp4"}
  with YoutubeDL() as ydl:
    ydl.download([url])

  video = open(f"{message.message_id}.mp4", "rb")

  try:
    await message.reply_video(video) 
  finally:
    video.close()
    os.remove(f"{message.message_id}.mp4")

  await message.delete()

app.run()