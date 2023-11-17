import telebot
import yt_dlp
from telebot import types

TOKEN = '5718397874:AAF09k95kIaD0W5rRSgmNa1gtwKs56WzIAU'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, please send url to stream it")
@bot.message_handler(commands=['sites'])
def sites_command_handler(message):
    bot.reply_to(message, f"`Here is` [supported sites](https://ytdl-org.github.io/youtube-dl/supportedsites.html)", disable_web_page_preview=True)
@bot.message_handler(func=lambda message: True)
def process_video(message):
    try:
        video_url = message.text
        ydl_opts = {'format': 'best'}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            stream_url = info_dict['url']

        # إنشاء رابط قابل للنقر باستخدام HTML
        markup = types.InlineKeyboardMarkup()
        btn_watch = types.InlineKeyboardButton(text='Watch', url=stream_url)
        markup.add(btn_watch)

        bot.reply_to(message, "Here is streaming link : ", reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, f"Error :  {str(e)}")

bot.infinity_polling()
