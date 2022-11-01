from bot.bot import Bot
from bot.handler import CommandHandler, BotButtonCommandHandler, MessageHandler
from bot.filter import Filter
import json
from io import StringIO


from cat.report.report import *
from cat.log import *
from cat.mdr.mdr import *


TOKEN = "001.1834776426.3374818595:1002701351"
bot = Bot(token=TOKEN)


def start(bot, event):
    write_log(event.from_chat, 'None')
    bot.send_text(chat_id=event.from_chat,
    text='Выберите категорию',
    inline_keyboard_markup='{}'.format(json.dumps([
        [{'text': 'MDR', 'callbackData': 'mdr(bot, event)', 'style': 'primary'}],
        [{'text': 'Отчетность', 'callbackData': 'report(bot, event)', 'style': 'primary'}]
    ])))


def buttons(bot, event):
    eval(event.data['callbackData'])


def main(bot, event):
    try:
        print('try:')
        print(event.from_chat)
        print(event.text)
        eval(read_log(event.from_chat))
    except:
        print('except')
        write_log(event.from_chat, 'None')


bot.dispatcher.add_handler(CommandHandler(command='start', callback=start))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons))
bot.dispatcher.add_handler(MessageHandler(filters=Filter.text, callback=main))
bot.start_polling()
bot.idle()