import os
from telebot import types
from datetime import date
from db.db import user_collection, plans_collection
from config import bot, start_date, scores, regular_tasks


def update_plans(data, user_name):
    result = plans_collection.find_one(
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
        plans_collection.insert_one(element)
        return True


def plans(message):
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
        response = update_plans(data, result["name"])

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
                print(result)
                data = result[week]
                data["plans"] += scores["Планирование"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                print("Элемент", element)
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                data_week['plans'] = scores["Планирование"]
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Планирование загружено",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня Планирование",
                             reply_markup=keyboard
                             )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        response = update_plans(data, result["name"])
        if response:
            try:
                print(result['plans'], scores["Планирование"])
                data = result['plans'] + scores["Планирование"]
                element = {
                    "$set": {
                        'plans': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                element = {
                    "$set": {
                        'plans': scores["Планирование"]
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Планирование загружено",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня Планирование",
                             reply_markup=keyboard
                             )
