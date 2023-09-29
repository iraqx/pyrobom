import os
import requests
import telebot
from pytube import YouTube, Search

API_TOKEN = '5718397874:AAGwjNGnv95LuBANzYOuGi4tu1CGe1e9r-c'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['s'])
def search(message):
    try:
        text = message.text
        text = text.split(' ')
        text.pop(0)
        searchText = ' '.join(text)
        s = Search(searchText)
        endUrl = s.results[0].watch_url
        download(endUrl, message)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Nothing found.')

@bot.message_handler(commands=['it', 'это'])
def direct_url(message):
    try:
        url = message.text.split(' ')[1]
        download(url, message)
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Something went wrong.')

def download(url, message):
    yt = YouTube(url) 
    if yt.length // 60 >= 30:
        bot.send_message(message.chat.id, f'The video is too long (more than 30 minutes)!\nCancel!\n{yt.watch_url}')
        return
    video = yt.streams.filter(abr='160kbps').last()
    ss = video.download()
    thumb = requests.get(yt.thumbnail_url).content
    os.rename(ss, f"{message.from_user.id}.mp3")

    audio = open(f"{message.from_user.id}.mp3", 'rb')
    bot.send_audio(message.chat.id, audio, title=yt.title, performer=yt.author, thumb=thumb)
    audio.close()
    os.remove(f'{os.getcwd()}/{message.from_user.id}.mp3')

bot.infinity_polling()
