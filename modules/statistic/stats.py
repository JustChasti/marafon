from datetime import date
from db.db import user_collection
from loguru import logger
import openpyxl
from datetime import datetime


excel_path = 'excel/stats.xlsx'


def get_beginer_week():
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    delta = date.today() - start_date
    delta = int(delta.days)
    if delta < 7:
        week = 'week 1'
    elif delta < 14:
        week = 'week 2'
    elif delta < 21:
        week = 'week 3'
    else:
        week = 'week 4'
    out_str = 'Статистика:\n'
    try:
        users = user_collection.find({'programm': 'beginer'})
        for i in users:
            data = i[week]
            sum = 0
            for j in data:
                sum += int(data[j])
            out_str += f'{i["name"]} - {sum}\n'
    except Exception as e:
        logger.exception(e)
    return out_str


def get_beginer_stats():
    out_str = 'Статистика:\n'
    try:
        users = user_collection.find({'programm': 'beginer'})
        for i in users:
            sum = 0
            try:
                sum += i['critical']
            except Exception as e:
                pass
            for j in i:
                if 'week' in j:
                    data = i[j]
                    for k in data:
                        sum += int(data[k])
            out_str += f'{i["name"]} - {sum}\n'
    except Exception as e:
        logger.exception(e)
    return out_str


def get_3program_stats(id):
    out_str = 'Статистика:\n'
    user = user_collection.find_one({'telegram_id': id})
    try:
        users = user_collection.find({'programm': user['programm']})
        for i in users:
            sum = 0
            for j in i:
                if j != 'telegram_id':
                    try:
                        sum += int(i[j])
                    except Exception as e:
                        pass
            out_str += f'{i["name"]} - {sum}\n'
    except Exception as e:
        logger.exception(e)
    return out_str


def get_all_stats():
    out_str = 'Статистика:\n'
    try:
        users = user_collection.find({})
        for i in users:
            sum = 0
            try:
                if i['programm'] == 'beginer':
                    try:
                        sum += i['critical']
                    except Exception as e:
                        pass
                    for j in i:
                        if 'week' in j:
                            data = i[j]
                            for k in data:
                                sum += int(data[k])
                else:
                    for j in i:
                        if j != 'telegram_id':
                            try:
                                sum += int(i[j])
                            except Exception as e:
                                pass
            except Exception as e:
                logger.info('user not registred')
            out_str += f'{i["name"]} - {sum}\n'
    except Exception as e:
        logger.exception(e)
    return out_str


def my_stats_excel(id):
    wb = openpyxl.load_workbook(filename=excel_path)
    sheet = wb.active
    sheet.title = 'Статистика'
    user = user_collection.find_one({'telegram_id': id})
    counter = 1
    for i in user:
        if i == '_id':
            pass
        elif 'week' in i:
            counter += 1
            sheet[f'A{counter}'] = i
            counter += 1
            for j in user[i]:
                sheet[f'B{counter}'] = j
                sheet[f'C{counter}'] = user[i][j]
                counter += 1
        else:
            sheet[f'A{counter}'] = i
            sheet[f'B{counter}'] = user[i]
            counter += 1
    wb.save(f'excel/{id}.xlsx')
    return f'excel/{id}.xlsx'


def my_stats(id):
    user = user_collection.find_one({'telegram_id': id})
    counter = 1
    out_str = ''
    for i in user:
        if i == '_id':
            pass
        elif 'week' in i:
            out_str += str(i)
            out_str += '\n'
            for j in user[i]:
                out_str += f'{j} - {user[i][j]}\n'
        else:
            if  i != '_id' and  i != 'programm':
                out_str += f'{i} - {user[i]}\n'
    return out_str
