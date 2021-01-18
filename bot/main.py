"""Main file of the bot"""
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from telebot import types, TeleBot
from flask import Flask, request

from bot import db_worker, utils

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = TeleBot(TOKEN)


# ------------ Bot functions start ---------- #
@bot.message_handler(commands=['start'])
def start_command(message):
    """Start command handler"""
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    get_text_item = types.KeyboardButton(utils.buttons_text['get_text'])
    add_text_item = types.KeyboardButton(utils.buttons_text['add_text'])
    markup.add(get_text_item, add_text_item)
    bot.send_message(
        message.chat.id,
        'Hello, how are you?',
        reply_markup=markup)


@bot.message_handler(commands=['remove'])
def remove_command(message):
    """Remove command handler"""
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        'Keyboard removed',
        reply_markup=hide_markup)


@bot.message_handler(commands=['add'])
def add_note(message):
    """Add command handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    data = message.text.split('\n')[1:]
    timestamp = time.time()  # get current time
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
        bot.send_message(
            chat_id,
            'Please, write you message correctly. Type /templates for help')
    sqlighter.close()


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
        bot.send_message(
            chat_id,
            'Please, write you command correctly. Type /templates for help')
    sqlighter.close()


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
        mark_item = types.InlineKeyboardButton(
            f'Mark as \"{utils.status_codes[note[3]].get("reverse_str")}\"',
            callback_data=f'mark{note[5]}{utils.status_codes[note[3]].get("int")}')
        edit_mark = types.InlineKeyboardButton(
            'Edit', callback_data=f'edit{note[5]}')
        delete_mark = types.InlineKeyboardButton(
            'Delete', callback_data=f'delete{note[5]}')
        markup.add(mark_item, edit_mark, delete_mark)

        bot.send_message(chat_id, msg, parse_mode='HTML', reply_markup=markup)
    sqlighter.close()


@bot.message_handler(commands=['statistics'])
def statistics_command(message):
    """Statistics command handler"""
    sqlighter = db_worker.SQLighter(os.getenv('DB_PATH'))
    chat_id = message.chat.id
    notes = sqlighter.get('chat_id', chat_id)
    ready_num = unready_num = 0
    for note in notes:
        if note[3]:
            ready_num += 1
        else:
            unready_num += 1
    data = {
        'all_num': len(notes),
        'unready_num': unready_num,
        'ready_num': ready_num}
    text = utils.statistics_template(data)
    bot.reply_to(message, 'Your statistics of all time:')
    bot.send_message(chat_id, text, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help_command(message):
    """Help command handler"""
    bot.send_message(message.chat.id, """
        /add - Add a new note
/get - Get all your notes
/edit - Edit a note
/templates - Show templates for /add and /edit commands
/remove - Remove a keyboard
/statistics - Show your statistics of all time
/help - List of all commands
    """)


@bot.message_handler(commands=['templates'])
def templates_command(message):
    """Templates command handler"""
    chat_id = message.chat.id
    # Add template
    bot.send_message(chat_id, 'Here is template for /add command:')
    bot.send_message(chat_id, """
        /add
_Header of a note_
_Text of a note_
_Due time to do_
    """, parse_mode='Markdown')
    # Edit template
    bot.send_message(chat_id, 'Here is template for /edit command:')
    bot.send_message(chat_id, """
        /edit
_ID of a note_
_Header of a note_
_Text of a note_
_Due time to do_
        """, parse_mode='Markdown')


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
            # Edit button pressed
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
            # Delete button pressed
            elif call.data.startswith(delete_str):
                sqlighter.delete(parameter, call.data[len(delete_str):])
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text='Deleted',
                    reply_markup=None)
            # Mark button pressed
            elif call.data.startswith(mark_str):
                value_to_set = call.data[-1]  # get value from call.data
                # get note id from call.data
                note_id = call.data[len(mark_str):len(call.data) - 1]
                sqlighter.update('status',
                                 value_to_set,
                                 'id',
                                 note_id)
                note = sqlighter.get('id', note_id)[0]  # get updated note
                if value_to_set == '1':  # Mark as "ready"
                    due_time = utils.get_time_obj(note[4])
                    now_timestamp = datetime.now().timestamp()
                    due_time_timestamp = datetime.timestamp(due_time)
                    if now_timestamp - due_time_timestamp > 0:
                        # Show bad alert
                        bot.answer_callback_query(
                            callback_query_id=call.id,
                            show_alert=True,
                            text='You did not have time to complete the task. Try better next time\N{grinning face}')
                    else:
                        # Show good alert
                        bot.answer_callback_query(
                            callback_query_id=call.id,
                            show_alert=True,
                            text='Hooray! You managed to complete the task on time. Do not slow down\N{flexed biceps}')

                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=utils.note_template(note),
                    parse_mode='HTML')

    except Exception as error:
        print(f'Error: {error}')
    sqlighter.close()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Echo all messages from user"""
    if message.text == utils.buttons_text['get_text']:
        help_command(message)
    elif message.text == utils.buttons_text['add_text']:
        bot.reply_to(message, 'Type /add command')
    else:
        bot.reply_to(message, 'I don\'t understand you. Please, type /help')

# ------------ Bot functions end ------------ #

# ------------ Webhooks start ------------ #
server = Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "!", 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://vtl-schedule-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    print('Bot started')
# ------------ Webhooks end -------------- #

# ------------ Polling start ------------- #
print('Bot started')
bot.polling(none_stop=True, interval=0)
# ------------ Polling end --------------- #
