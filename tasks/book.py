from telebot import types
from datetime import date
from db.db import user_collection, books_collection
from config import bot, start_date, scores, regular_tasks
from keyboards import keyboard_mind


def update_book(data, user_name):
    element = {
        'user': user_name,
        'data': data

    }
    books_collection.insert_one(element)


def menu(message):
    if message.text == 'Подтвердить':
        bot.send_message(message.from_user.id,
                         "Напишите название",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, book)
    else:
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_mind
                         )


def book(message):
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
        update_book(data, message.from_user.id)

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
            data["book"] += scores["Книга"]
            element = {
                "$set": {
                    week: data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            data_week = regular_tasks
            data_week['book'] = scores["Книга"]
            element = {
                "$set": {
                    week: data_week
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                            "Книга засчитана",
                            reply_markup=keyboard
                            )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = message.text
        update_book(data, message.from_user.id)
        try:
            data = result['book'] + scores["Книга"]
            element = {
                "$set": {
                    'book': data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            element = {
                "$set": {
                    'book': scores["Книга"]
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                            "Книга засчитана",
                            reply_markup=keyboard
                            )
