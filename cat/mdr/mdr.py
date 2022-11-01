import json
from cat.mdr.mdr016 import *

def mdr(bot, event):
    bot.send_text(chat_id=event.from_chat,
    text='Выберите проект:',
    inline_keyboard_markup='{}'.format(json.dumps([[
        {'text': '016-Гидрополимет', 'callbackData': 'mdr_016(bot, event)', 'style': 'primary'}
    ]])))