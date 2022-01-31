from telebot import types
from datetime import date
from db.db import user_collection
from config import bot, start_date, scores, regular_tasks, fit_games
from modules.keyboards import keyboard_switch, keyboard_fit_game


def game_switch(message):
    if 'уровень' in message.text:
        data = message.text.split(' ')[0]
        bot.send_message(
            message.from_user.id,
            fit_games[int(data)-1],
            reply_markup=keyboard_switch
        )
        bot.register_next_step_handler(message, menu, data=data)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Мышление')
        button2 = types.KeyboardButton('Здоровье')
        button3 = types.KeyboardButton('Статистика')
        keyboard.add(button1, button2, button3)
        bot.send_message(
            message.from_user.id,
            "Ошибка",
            reply_markup=keyboard
        )


def menu(message, data):
    if message.text == 'Подтвердить':
        game(message, data)
    else:
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_fit_game
                         )
        bot.register_next_step_handler(message, game_switch)


def game(message, ball):
    print(ball)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    button3 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3)

    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if result["programm"] == "beginer":
        delta = date.today() - start_date
        delta = int(delta.days)
        data = ball * 10

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
            data["fitness-game"] += int(ball) * 10
            element = {
                "$set": {
                    week: data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            data_week = regular_tasks
            data_week['fitness-game'] = int(ball) * 10
            element = {
                "$set": {
                    week: data_week
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                         "Введите время в формате ММ:СС (например 12:05 - 12 минут 5 секунд)",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

    else:
        delta = date.today() - start_date
        delta = int(delta.days)
        data = ball * 10
        try:
            data = result['fitneess-game'] + int(ball) * 10
            element = {
                "$set": {
                    'fitness-game': data
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        except KeyError as e:
            element = {
                "$set": {
                    'fitness-game': int(ball) * 10
                }
            }
            user_collection.update_one({'_id': result["_id"]}, element)
        bot.send_message(message.from_user.id,
                         "Введите время в формате ММ:СС (например 12:05 - 12 минут 5 секунд)",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
    bot.register_next_step_handler(message, get_time_ball, ball)


def get_time_ball(message, ball):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    button3 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3)
    print(message.text)
    bot.send_message(
        message.from_user.id,
        "Вы зарегистрировали фитнес игру",
        reply_markup=keyboard
    )
