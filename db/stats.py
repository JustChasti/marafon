from datetime import date
from db.db import user_collection
from config import start_date
from loguru import logger


def get_beginer_week():
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
