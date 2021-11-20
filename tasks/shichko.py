import os
from telebot import types
from datetime import date
from db.db import user_collection, shichko_collection
from config import bot, start_date, scores


def update_shihcko(data, user_name):
    result = shichko_collection.find_one(
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
        shichko_collection.insert_one(element)
        return True


def shichko(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    keyboard.add(button1, button2)

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
            elif delta < 14:
                week = 'week 3'
            else:
                week = 'week 4'
            try:
                print(result)
                data = result[week]
                data["shichko"] += scores["Шичко"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                print("Элемент", element)
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                element = {
                    "$set": {
                        week: {
                            'shichko': scores["Шичко"],
                            'planning': 0,
                            'thanks': 0,
                            'main_task': 0,
                            'book': 0,
                            'audio_book': 0,
                            'analyzes': 0,
                            'sport': 0,
                            'jogging': 0,
                            'walk': 0
                        }
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
        pass
        bot.send_message(message.from_user.id,
                         "Шичко загружен",
                         reply_markup=keyboard
                         )
