from bot.handler import MessageHandler
from bot.filter import Filter
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from cat.log import *


creds = service_account.Credentials.from_service_account_file('cat/key.json')
service = build('sheets', 'v4', credentials=creds)
spreadsheetId = '1q9bHbkFARdWuOeqZYkdKfFFFkfA9wfJUrSZ4Eh3spCs'

report_dict = {}
sheets = {}

sheets_list = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
for i in sheets_list['sheets']:
    sheets[i['properties']['title']] = i['properties']['sheetId']


# Main functions
def val_append(dict, key, value):
    tmp = dict[key]
    if type(tmp) == list:
        pass
    else:
        tmp = list(str(dict[key]))
    tmp.append(value)
    dict.update({key:tmp})


def report(bot, event):
    try:
        report_dict.pop(event.from_chat)
    except:
        pass
    bot.send_text(chat_id=event.from_chat,
    text='Выберите проект',
    inline_keyboard_markup='{}'.format(json.dumps([[
        {'text': '016-Гидрополимет', 'callbackData': 'report_016_weeks(bot, event)', 'style': 'primary'}
    ]])))
# Main functions

# Project 016
def report_016_weeks(bot, event):
    bot.send_text(chat_id=event.from_chat,
    text='Проект:' + \
        '\n016-Гидрополимет' + \
        '\n\nСсылка на отчет:' + \
        '\nhttps://docs.google.com/spreadsheets/d/' + spreadsheetId + \
        '\n\nВыберите неделю',
    inline_keyboard_markup='{}'.format(json.dumps([        
        [{'text': 'Week-6 (17.10.2022-23.10.2022)', 'callbackData': 'check_dub_016(bot, event, 6)', 'style': 'primary'}],
        [{'text': 'Week-7 (24.10.2022-30.10.2022)', 'callbackData': 'check_dub_016(bot, event, 7)', 'style': 'primary'}]        
    ])))

def check_dub_016(bot, event, week):
    report_dict[event.from_chat] = week
    column_A = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range='Week-{}!A:A'.format(week)).execute()
    column_A = column_A.get('values', [])

    if [event.message_author] in column_A:
        bot.send_text(chat_id=event.from_chat,
        text='Вы уже уже заполнили отчет за эту неделю!',
        inline_keyboard_markup='{}'.format(json.dumps([
            [{'text': 'Домой', 'callbackData': 'start(bot, event)', 'style': 'primary'}],
            [{'text': 'Перезаписать отчет', 'callbackData': 'report_change_016(bot, event)', 'style': 'primary'}]
        ])))
    else:
        report_016_hours(bot, event)


def report_change_016(bot, event):
    print('check')
    print(report_dict)
    column_A = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range='Week-{}!A:A'.format(report_dict[event.from_chat])).execute()
    column_A = column_A.get('values', [])
    print('check1')
    values = [{
        'deleteDimension': {
            'range': {
                'sheetId': sheets['Week-{}'.format(report_dict[event.from_chat])],
                'dimension': 'ROWS',
                'startIndex': column_A.index([event.from_chat]),
                'endIndex': column_A.index([event.from_chat])+1
            }
        }
    }]
    print('check2')
    body = {'requests': values}
    result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()
    report_016_hours(bot, event)
    print('check3')


def report_016_hours(bot, event): 
    bot.send_text(chat_id=event.from_chat,
    text='Напишите сколько часов было потрачено')
    write_log(event.from_chat, 'report_016_hours_check(bot, event)')

def report_016_hours_check(bot, event):
    if type(report_dict[event.from_chat]) == list:
        report_dict[event.from_chat][1] = event.text
    else:
        val_append(report_dict, event.from_chat, event.text)
    bot.send_text(chat_id=event.from_chat,
    text='Проверьте, вы правильно ввели данные?',
    inline_keyboard_markup='{}'.format(json.dumps([
        [{'text': 'Да, продолжить', 'callbackData': 'report_016_gettext(bot, event)', 'style': 'primary'}],
        [{'text': 'Нет, перезаписать', 'callbackData': 'report_016_hours(bot, event)', 'style': 'primary'}]
    ])))

def report_016_gettext(bot, event):
    bot.send_text(chat_id=event.from_chat,
    text='Введите выполненные работы')
    write_log(event.from_chat, 'report_016_gettext_check(bot, event)')

def report_016_gettext_check(bot, event):
    if type(report_dict[event.from_chat]) == list and len(report_dict[event.from_chat]) == 5:
        report_dict[event.from_chat][2] = event.text
    else:
        val_append(report_dict, event.from_chat, event.text)
        val_append(report_dict, event.from_chat, event.message_author['firstName'])
        val_append(report_dict, event.from_chat, event.message_author['lastName'])
    bot.send_text(chat_id=event.from_chat,
    text='Проверьте, вы правильно ввели данные?',
    inline_keyboard_markup='{}'.format(json.dumps([
        [{'text': 'Да, продолжить', 'callbackData': 'report_016(bot, event)', 'style': 'primary'}],
        [{'text': 'Нет, перезаписать', 'callbackData': 'report_016_gettext(bot, event)', 'style': 'primary'}]
    ])))

def report_016(bot, event):
    print('check1')
    # Last Row
    column_A = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId,
                range='Week-{}!A:A'.format(report_dict[event.from_chat][0])).execute()
    column_A = column_A.get('values', [])    
    last_row = len(column_A)+1
    # Last Row
    print('check2')
    range = 'Week-{0}!A{1}:D{1}'.format(report_dict[event.from_chat][0], last_row)
    valueInputOption = 'USER_ENTERED'
    print('check3')
    values = [
        [event.from_chat,
        report_dict[event.from_chat][3]+" "+report_dict[event.from_chat][4],
        report_dict[event.from_chat][1],
        report_dict[event.from_chat][2]]
    ]
    print('check4')
    body = {'values': values}
    
    result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheetId, range=range,
                valueInputOption=valueInputOption, body=body).execute()

    bot.send_text(chat_id=event.from_chat,
    text='Данные успешно добавлены!')
    print('check5')
    write_log(event.from_chat, 'None')
    #print(f"{result.get('updatedCells')} cells updated.")
# Project 016