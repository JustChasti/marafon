import os
from telebot import types
from datetime import date
from db.db import user_collection, shichko_collection
from config import bot, start_date, scores, regular_tasks
from keyboards import keyboard_mind


def update_shihcko(data, user_name):
    element = {
        'user': user_name,
        'date': str(date.today()),
        'data': data

    }
    shichko_collection.insert_one(element)
    return True


def menu(message):
    if message.text == 'Подтвердить':
        bot.send_message(message.from_user.id,
                         "Загрузите Шичко",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, shichko)
    else:
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_mind
                         )


def shichko(message):
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
            name = f'{path}/{date.today()}-shichko.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_shihcko(name, result["name"])
        else:
            data = message.text
            response = update_shihcko(data, result["name"])

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
                data["shichko"] += scores["Шичко"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                data_week['shichko'] = scores["Шичко"]
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Шичко загружен",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня Шичко",
                             reply_markup=keyboard
                             )

    else:
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            path = message.from_user.id
            name = f'{path}/{date.today()}-shichko.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_shihcko(name, result["name"])
        else:
            data = message.text
            response = update_shihcko(data, result["name"])

        if response:
            try:
                data = result['shichko'] + scores["Шичко"]
                element = {
                    "$set": {
                        'shichko': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                element = {
                    "$set": {
                        'shichko': scores["Шичко"]
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Шичко загружен",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня Шичко",
                             reply_markup=keyboard
                             )
