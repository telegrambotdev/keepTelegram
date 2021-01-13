"""Main file of the bot"""
import os
import time

from dotenv import load_dotenv
from telebot import types, TeleBot

from bot import db_worker, utils

load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))


# ------------ Bot functions start ---------- #
@bot.message_handler(commands=['help'])
def help_command(message):
    """Help command handler"""
    bot.reply_to(message, 'Hello, how are you?')


@bot.message_handler(commands=['add'])
def add_note(message):
    """Add command handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    timestamp = time.time()
    if len(data) == 3:
        note = sqlighter.get('id', timestamp)
        if not note:
            if utils.get_time_obj(data[2]):
                sqlighter.add([
                    chat_id, data[0], data[1], 0, data[2], timestamp])
                bot.send_message(
                    chat_id, f'Your note with the header \"{data[0]}\" has been added')
            else:
                bot.send_message(
                    chat_id,
                    '<strong>Error!</strong> Enter the <i>datetime</i> field correctly',
                    parse_mode='HTML')
        else:
            bot.send_message(
                chat_id, f'Note with the header \"{data[0]}\" exists')
    else:
        bot.send_message(chat_id, 'Please, write you message correctly')
    sqlighter.close()
    print('Closing connection is successful')


@bot.message_handler(commands=['edit'])
def edit_note(message):
    """Edit command handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    if len(data) == 4:
        note = sqlighter.get('id', data[0])
        if note:
            if utils.get_time_obj(data[3]):
                for i in range(len(utils.note_fields)):
                    sqlighter.update(
                        utils.note_fields[i], data[i + 1], 'id', data[0])
                bot.send_message(
                    chat_id,
                    f'Your note with new header \"<strong>{data[1]}</strong>\" has been updated',
                    parse_mode='HTML')
            else:
                bot.send_message(
                    chat_id,
                    '<strong>Error!</strong> Enter the <i>datetime</i> field correctly',
                    parse_mode='HTML')
        else:
            bot.send_message(
                chat_id,
                f'Note with ID <i>{data[0]}</i> doesn\'t exists. Please check it',
                parse_mode='HTML')
    else:
        bot.send_message(chat_id, 'Please, write you command correctly')
    sqlighter.close()
    print('Closing connection is successful')


@bot.message_handler(commands=['get'])
def get_notes(message):
    """Get command handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    bot.reply_to(message, 'Your notes:')
    chat_id = message.chat.id
    data = sqlighter.get('chat_id', chat_id)
    for note in data:
        msg = utils.note_template(note)  # message template

        # Markup for note
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton(
            f'Mark as \"{utils.status_codes[note[3]].get("reverse_str")}\"',
            callback_data=f'mark{note[5]}{utils.status_codes[note[3]].get("int")}')
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
    """Callbacks handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    parameter = 'id'
    edit_str = 'edit'
    delete_str = 'delete'
    mark_str = 'mark'
    try:
        if call.message:
            if call.data.startswith(edit_str):
                bot.send_message(
                    call.message.chat.id,
                    'Edit this note with ID and /edit command')
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
                sqlighter.update('status',
                                 call.data[-1],
                                 'id',
                                 call.data[len(mark_str):len(call.data) - 1])
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='State updated',
                    reply_markup=None)

    except Exception as error:
        print(f'Error: {error}')
    sqlighter.close()
    print('Closing connection is successful')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Echo all messages from user"""
    bot.reply_to(message, message.text)

# ------------ Bot functions end ------------ #


print("Bot started")
bot.polling(none_stop=True, interval=0)
