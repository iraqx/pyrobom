import os
os.system("pip install telebot")
import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
TOKEN = '5781017151:AAH3ErhLd1Up3ig_-yyNF4ys9KWZnYhRlVA'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['ping'])
def send_pong(message):
    bot.reply_to(message, 'Pong!')

if __name__ == '__main__':
    bot.polling(none_stop=True)
    
