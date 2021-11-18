from os import name
from config import bot
from loguru import logger
from telebot import *
from db.db import user_collection


@bot.message_handler(commands=['help', 'start'])
def start_chat(message):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if result:
        bot.send_message(message.from_user.id,
                         "Вы уже зарегестрированы - работайте по программе"
                         )
    else:
        bot.send_message(message.from_user.id,
                         "Введите ваше имя"
                         )
        bot.register_next_step_handler(message, registration)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if not result:
        bot.send_message(message.from_user.id,
                         "Вы незарегистрированы"
                         )
    elif message.text == 'Мышление':
        bot.send_message(message.from_user.id,
                         "Мышление"
                         )
    elif message.text == 'Здоровье':
        bot.send_message(message.from_user.id,
                         "Здоровье"
                         )
    else:
        pass

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
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Новичок', callback_data='beginer')
        button2 = types.InlineKeyboardButton('Старт', callback_data='starter')
        button3 = types.InlineKeyboardButton('Профи', callback_data='profi')
        button4 = types.InlineKeyboardButton('Лидер', callback_data='leader')
        keyboard.add(button1, button2, button3, button4)
        bot.send_message(message.from_user.id,
                         "Теперь выбери свой этап. Если ты выпуснкик, то можешь выбрать любой из этапов",
                         reply_markup=keyboard
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

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Мышление')
        button2 = types.KeyboardButton('Здоровье')
        keyboard.add(button1, button2)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Новичок",
                         reply_markup=keyboard
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )

bot.polling(none_stop=True)
