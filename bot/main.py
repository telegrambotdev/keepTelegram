from bot import dbWorker
import os
import time
import telebot
from dotenv import load_dotenv
load_dotenv()


bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, how are you?")


@bot.message_handler(commands=['add'])
def add_note(message):
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    timestamp = time.time()
    print(data)
    if len(data) == 3:
        conn = dbWorker.connect(os.getenv("DB_PATH"))
        note = dbWorker.get(conn.cursor(), 'id', timestamp)
        if not note:
            dbWorker.add(
                conn, conn.cursor(), [
                    chat_id, data[0], data[1], 0, data[2], timestamp])
            conn.close()
            bot.send_message(chat_id, f'Your note with the header \"{data[0]}\" has been added')
        else:
            bot.send_message(chat_id, f'Note with the header \"{data[0]}\" exists')
    else:
        bot.send_message(chat_id, 'Please, write you message correctly')
    print('Closing connection is successful')


@bot.message_handler(commands=['get'])
def get_notes(message):
    conn = dbWorker.connect(os.getenv("DB_PATH"))
    data = dbWorker.get(conn.cursor(), 'test_id')
    bot.reply_to(message, "Hello, how are you?")
    conn.close()
    print('Data is: ', data)
    print('Closing connection is successful')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


print("Bot started")
bot.polling(none_stop=True, interval=0)
