from telebot import types
from datetime import date
from db.db import user_collection, lessons_collection
from config import bot, start_date, scores, regular_tasks
from keyboards import keyboard_mind


def update_lessons(data, user_name):
    element = {
        'user': user_name,
        'date': str(date.today()),
        'data': data

    }
    lessons_collection.insert_one(element)
    return True


def menu(message):
    if message.text == 'Подтвердить':
        bot.send_message(message.from_user.id,
                         "Прямой Эфир засчитан",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        stream(message)
    else:
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_mind
                         )


def stream(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    button3 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3)

    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if result["programm"] == "beginer":
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        response = update_lessons(data, result["name"])

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
                data["stream"] += scores["Прямой эфир"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                data_week['stream'] = scores["Прямой эфир"]
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Вы посетили прямой эфир",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже посещали прямой эфир сегодня",
                             reply_markup=keyboard
                             )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        response = update_lessons(data, result["name"])
        if response:
            try:
                data = result['stream'] + scores["Прямой эфир"]
                element = {
                    "$set": {
                        'stream': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                element = {
                    "$set": {
                        'stream': scores["Прямой эфир"]
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Вы посетили прямой эфир",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже посещали прямой эфир сегодня",
                             reply_markup=keyboard
                             )