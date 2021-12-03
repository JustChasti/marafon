from telebot import types
from datetime import date
from db.db import user_collection, clean_collection
from config import bot, start_date, scores, regular_tasks


def update_clean(data, user_name):
    result = clean_collection.find_one(
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
        clean_collection.insert_one(element)
        return True


def register_clean(message):
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
        response = update_clean(data, result["name"])

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
                data = result[week]
                if (week == 'week 1') or (week == 'week 2'):
                    data["clean"] += scores["Чистый день 1"]
                else:
                    data["clean"] += scores["Чистый день 2"]
                element = {
                    "$set": {
                        week: data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                if (week == 'week 1') or (week == 'week 2'):
                    data_week['clean'] = scores["Чистый день 1"]
                else:
                    data_week['clean'] = scores["Чистый день 2"]
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Вы зарегистрировали чистый день",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже зарегистрировали чистый день сегодня",
                             reply_markup=keyboard
                             )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        response = update_clean(data, result["name"])
        if response:
            try:
                if delta < 14:
                    data = result['clean'] + scores["Чистый день 1"]
                else:
                    data = result['clean'] + scores["Чистый день 2"]
                element = {
                    "$set": {
                        'clean': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                if delta < 14:
                    element = {
                        "$set": {
                            'clean': scores["Чистый день 1"]
                        }
                    }
                else:
                    element = {
                        "$set": {
                            'clean': scores["Чистый день 2"]
                        }
                    }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Вы зарегистрировали чистый день",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже зарегистрировали чистый день сегодня",
                             reply_markup=keyboard
                             )
