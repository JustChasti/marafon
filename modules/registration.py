from telebot import types

from config import bot
from db.db import user_collection
from modules.keyboards import keyboard_main, keyboard_programs


def registration(message):
    result = user_collection.find_one({'name': message.text})
    if result:
        element = {
            "$set": {
                'telegram_id': message.from_user.id
            }
        }
        user_collection.update_one({'name': message.text}, element)
        bot.send_message(message.from_user.id,
                         "Добро пожаловать на Марафон"
                         )
        bot.send_message(message.from_user.id,
                         "Теперь выбери свой этап. Если ты выпуснкик, то можешь выбрать любой из этапов",
                         reply_markup=keyboard_programs
                         )
    else:
        bot.send_message(message.from_user.id,
                         "Вы не доавлены в проект: Обратитесь к Никите(https://t.me/nixon49) или к разработчику (https://t.me/kot_gray)"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'beginer')
def process_callback_button1(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Новичок") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'beginer'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Новичок",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'starter')
def process_callback_button2(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Старт") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'start'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Старт",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'profi')
def process_callback_button3(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Эксперт") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'profi'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Эксперт",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'leader')
def process_callback_button4(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Лидер") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'leader'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Лидер",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )
