from bot import dbWorker
import os
import time
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
# ------------ Program variable start ----------- #
bot = telebot.TeleBot(os.getenv("TOKEN"))
status_codes = {
    0: {'str': 'ready', 'int': 1},
    1: {'str': 'unready', 'int': 0},
}
# ------------ Program variables end ------------ #


# ------------ Program functions start ---------- #
def note_template(data):
    return f"""
<strong>Header</strong>: <i>{data[1]}</i>
<strong>Text</strong>: <i>{data[2]}</i>
<strong>Status</strong>: <i>{data[3]}</i>
<strong>Due time</strong>: <i>{data[4]}</i>
"""
# ------------ Program functions end ------------ #


# ------------ Bot functions start ---------- #
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Hello, how are you?')


@bot.message_handler(commands=['add'])
def add_note(message):
    sqlighter = dbWorker.SQLighter(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    timestamp = time.time()
    if len(data) == 3:
        note = sqlighter.get('id', timestamp)
        if not note:
            sqlighter.add([
                chat_id, data[0], data[1], 0, data[2], timestamp])
            sqlighter.close()
            bot.send_message(
                chat_id, f'Your note with the header \"{data[0]}\" has been added')
        else:
            bot.send_message(
                chat_id, f'Note with the header \"{data[0]}\" exists')
    else:
        bot.send_message(chat_id, 'Please, write you message correctly')
    print('Closing connection is successful')


@bot.message_handler(commands=['get'])
def get_notes(message):
    sqlighter = dbWorker.SQLighter(os.getenv('DB_PATH'))
    bot.reply_to(message, 'Your notes:')
    chat_id = message.chat.id
    data = sqlighter.get('chat_id', chat_id)
    for note in data:
        msg = note_template(note)  # message template

        # Markup for note
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton(
            f'Mark as \"{status_codes[note[3]].get("str")}\"', callback_data=f'mark{note[5]}{status_codes[note[3]].get("int")}')
        item2 = types.InlineKeyboardButton(
            'Edit', callback_data=f'edit{note[5]}')
        item3 = types.InlineKeyboardButton(
            'Delete', callback_data=f'delete{note[5]}')
        markup.add(item1, item2, item3)

        bot.send_message(chat_id, msg, parse_mode='HTML', reply_markup=markup)
    sqlighter.close()
    print('Closing connection is successful')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    sqlighter = dbWorker.SQLighter(os.getenv('DB_PATH'))
    parameter = 'id'
    edit_str = 'edit'
    delete_str = 'delete'
    mark_str = 'mark'
    try:
        if call.message:
            if call.data.startswith(edit_str):
                bot.send_message(call.message.chat.id, 'Edit this note with ID and /edit command')
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f'Note <strong>ID</strong>: <i>{call.data[len(edit_str):]}</i>',
                    reply_markup=None,
                    parse_mode='HTML')
            elif call.data.startswith(delete_str):
                sqlighter.delete(parameter, call.data[len(delete_str):])
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='Deleted',
                    reply_markup=None)
            elif call.data.startswith(mark_str):
                sqlighter.update('status', call.data[-1], 'id', call.data[len(mark_str):len(call.data)-1])
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='State updated',
                    reply_markup=None)

    except Exception as e:
        print(f'Error: {e}')
    sqlighter.close()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# ------------ Bot functions end ------------ #


print("Bot started")
bot.polling(none_stop=True, interval=0)
