from bot import dbWorker
import os
import telebot
from dotenv import load_dotenv
load_dotenv()


bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you?")


@bot.message_handler(commands=['add'])
def add_note(message):
    conn = dbWorker.connect(os.getenv("DB_PATH"))
    chat_id = message.chat.id
    print(message.text.split('\n'))
    if len(message.text.split('\n')) == 2:
        bot.send_message(chat_id, "good")
    else:
        bot.send_message(chat_id, "bad")
    # dbWorker.add_note(
    #     conn, conn.cursor(), [
    #         chat_id, 'test_header', 'test_text', 0, 'test_time'])
    conn.close()
    print('Closing connection is successful')


@bot.message_handler(commands=['get'])
def get_notes(message):
    conn = dbWorker.connect(os.getenv("DB_PATH"))
    data = dbWorker.get_notes(conn.cursor(), 'test_id')
    bot.reply_to(message, "Hello, how are you?")
    conn.close()
    print('Data is: ', data)
    print('Closing connection is successful')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


print("Bot started")
bot.polling(none_stop=True, interval=0)
