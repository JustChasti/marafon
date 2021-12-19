from telebot import types
from datetime import date
from db.db import user_collection
from config import bot, start_date, scores, regular_tasks


def game(message):
    print(message.text)
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
            data["fitness-game"] += int(message.text)
            element = {
                "$set": {
                    week: data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            data_week = regular_tasks
            data_week['fitness-game'] = int(message.text)
            element = {
                "$set": {
                    week: data_week
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                         "Фитнесс игра засчитана",
                         reply_markup=keyboard
                         )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        try:
            data = result['fitneess-game'] + int(message.text)
            element = {
                "$set": {
                    'fitness-game': data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            element = {
                "$set": {
                    'fitness-game': int(message.text)
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                         "Фитнесс игра засчитана",
                         reply_markup=keyboard
                         )
