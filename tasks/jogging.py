import os
from telebot import types
from datetime import date
from db.db import user_collection, run_walk_collection
from config import bot, start_date, scores, regular_tasks


def update_run(data, user_name):
    result = run_walk_collection.find_one(
        {
            'user': user_name,
            'date': str(date.today())
        }
    )
    if result:
        return False
    else:
        element = {
            'user': user_name,
            'date': str(date.today()),
            'data': data

        }
        run_walk_collection.insert_one(element)
        return True


def run_walk(message, run):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    button3 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3)

    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if result["programm"] == "beginer":
        delta = date.today() - start_date
        delta = int(delta.days)
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            path = message.from_user.id
            name = f'{path}/{date.today()}-run.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_run(name, result["name"])
        else:
            data = message.text
            response = update_run(data, result["name"])

        if response:
            if delta < 7:
                week = 'week 1'
            elif delta < 14:
                week = 'week 2'
            elif delta < 21:
                week = 'week 3'
            else:
                week = 'week 4'
            try:
                data = result[week]
                if run:
                    data["run-walk"] += scores["Пробежка"]
                else:
                    data["run-walk"] += scores["Прогулка"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                if run:
                    data_week['run-walk'] = scores["Пробежка"]
                else:
                    data["run-walk"] = scores["Прогулка"]
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Пробежка/прогулка загружена",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже загрузили сегодня пробежку/прогулку",
                             reply_markup=keyboard
                             )

    else:
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            path = message.from_user.id
            name = f'{path}/{date.today()}-run.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_run(name, result["name"])
        else:
            data = message.text
            response = update_run(data, result["name"])

        if response:
            try:
                if run:
                    data = result['run-walk'] + scores["Пробежка"]
                else:
                    data = result['run-walk'] + scores["Прогулка"]
                element = {
                    "$set": {
                        'sport': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                if run:
                    element = {
                        "$set": {
                            'run-walk': scores["Пробежка"]
                        }
                    }
                else:
                    element = {
                        "$set": {
                            'run-walk': scores["Прогулка"]
                        }
                    }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Пробежка/прогулка загружена",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы загрузили делали сегодня пробежку/прогулку",
                             reply_markup=keyboard
                             )
