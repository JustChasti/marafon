from telebot import types
from datetime import date
from db.db import user_collection, clean_collection
from config import bot, start_date, scores, videolections
from modules.keyboards import keyboard_mind, keyboard_mind


def spisok(message, text):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    programm = result["programm"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in videolections:
        if i['date'] <= date.today():
            button = types.KeyboardButton(i['name'])
            keyboard.add(button)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    bot.send_message(
        message.from_user.id,
        text,
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, handler)


def handler(message):
    if message.text == 'Назад':
        bot.send_message(
            message.from_user.id,
            "Назад",
            reply_markup=keyboard_mind
        )
    else:
        flag = True
        for i in videolections:
            if i['name'] == message.text:
                spisok(message, i['link'])
                flag = False
                break
        if flag:
            bot.send_message(
                message.from_user.id,
                "Такого видео нет",
                reply_markup=keyboard_mind
            )
