import telebot
from dotenv import load_dotenv

load_dotenv()
import os

bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


print("Bot started")
bot.polling(none_stop=True, interval=0)
