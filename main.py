import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['ping'])
def send_pong(message):
    bot.reply_to(message, 'Pong!')

if __name__ == '__main__':
    bot.polling(none_stop=True)
    
