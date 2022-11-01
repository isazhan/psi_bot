from cat.log import *
from io import StringIO
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

def mdr_016(bot, event):
    spreadsheetId = '1qoCQ69w3Fw68anz4d-Hj5Fnl0VAjg3jcUOHyXeQ4_24'
    bot.send_text(chat_id=event.from_chat,
    text='Ссылка на MDR:' + \
        '\nhttps://docs.google.com/spreadsheets/d/' + spreadsheetId)

    bot.send_text(chat_id=event.from_chat,
    text='Напишите список чертежей, которые хотите добавить в MDR')
    write_log(event.from_chat, 'mdr_016_check(bot,event)')


def mdr_016_check(bot, event):
    drawings = StringIO(event.text)
    df = pd.read_csv(drawings, sep='  ', header=None, dtype='string', engine='python')
    d0 = df.copy()
    print(1)
    creds = service_account.Credentials.from_service_account_file('cat/key.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheetId = '1qoCQ69w3Fw68anz4d-Hj5Fnl0VAjg3jcUOHyXeQ4_24'
    print(2)
    # Dis
    dis = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Data!A:A').execute()
    dis = dis.get('values', [])

    # Doc
    doc = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Data!B:B').execute()
    doc = doc.get('values', [])

    # Dis_Doc
    dis_doc = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Data!C:C').execute()
    dis_doc = dis_doc.get('values', [])

    # Dis_mark
    dis_mark = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='Data!D:D').execute()
    dis_mark = dis_mark.get('values', [])
    print(3)
    d0['prj number'] = d0[0].apply(lambda x: True if x=='016' else False)
    d0['dis check'] = d0[3].apply(lambda x: True if [x] in dis else False)
    d0['doc check'] = d0[4].apply(lambda x: True if [x] in doc else False)
    d0['dis-doc check'] = (d0[3]+'*'+d0[4]).apply(lambda x: True if [x] in dis_doc else False)
    d0['dis-mark check'] = (d0[3]+'*'+d0[7]).apply(lambda x: True if [x] in dis_mark else False)
    print(4)
    if d0.shape[0]*5 == d0.iloc[:, 9].sum() + d0.iloc[:, 10].sum() + d0.iloc[:, 11].sum() + d0.iloc[:, 12].sum() + d0.iloc[:, 13].sum():
        mdr_016_add(df)
        bot.send_text(chat_id=event.from_chat,
        text='Данные успешно добавлены!')
    else:
        bot.send_text(chat_id=event.from_chat,
        text='Имеются ошибки!')
        bot.send_text(chat_id=event.from_chat,
        text=d0.to_string())
    write_log(event.from_chat, 'None')


def mdr_016_add(df):
    creds = service_account.Credentials.from_service_account_file('cat/key.json')
    service = build('sheets', 'v4', credentials=creds)
    spreadsheetId = '1qoCQ69w3Fw68anz4d-Hj5Fnl0VAjg3jcUOHyXeQ4_24'

    # Last row
    row = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='MDR!H:H').execute()
    row = row.get('values', [])
    last_row = len(row)+1
    # Last row

    h = []
    for i in range(df.shape[0]):
        h.append('=A{0}&{1}-{1}&B{0}&{1}-{1}&C{0}&{1}-{1}&D{0}&{1}-{1}&E{0}&{1}-{1}&F{0}&{1}-{1}&G{0}'.format(i+last_row, '"'))
    df.insert(7, 'Document', h)

    j = []
    for i in range(df.shape[0]):
        j.append('=A{0}&{1}-{1}&B{0}&{1}-{1}&I{0}'.format(i+last_row, '"'))
    df.insert(9, 'GOST', j)

    k = []
    for i in range(df.shape[0]):
        k.append('PSI')
    df.insert(10, 'Resp', k)

    ran = 'MDR!A{}'.format(last_row)
    valueInputOption = 'USER_ENTERED'

    values = df.values.tolist()

    body = {'values': values}

    result = service.spreadsheets().values().update(
                    spreadsheetId=spreadsheetId, range=ran,
                    valueInputOption=valueInputOption, body=body).execute()