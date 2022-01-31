from telebot import types
from datetime import date, datetime
from db.db import user_collection, lessons_collection
from config import bot, scores, regular_tasks
from modules.keyboards import keyboard_mind


def update_lessons(data, user_name):
    return True


def menu(message):
    if message.text == 'Подтвердить':
        bot.send_message(message.from_user.id,
                         "Душ засчитан",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        stream(message)
    else:
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_mind
                         )


def stream(message):
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
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
            data["shower"] += scores["Душ"]
            element = {
                "$set": {
                    week: data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            data_week = regular_tasks
            data_week['shower'] = scores["Душ"]
            element = {
                "$set": {
                    week: data_week
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(
            message.from_user.id,
            "Вы зарегистрировали контрастный душ",
            reply_markup=keyboard
        )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        try:
            data = result['shower'] + scores["Душ"]
            element = {
                "$set": {
                    'shower': data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            element = {
                "$set": {
                    'shower': scores["Душ"]
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(
            message.from_user.id,
            "Вы зарегистрировали контрастный душ",
            reply_markup=keyboard
        )
