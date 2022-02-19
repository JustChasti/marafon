from telebot import types
from datetime import date
import datetime
from db.db import user_collection
from config import bot
from modules.keyboards import keyboard_video

def get_videolections():
    f = open('modules/reminder/data/videolections.txt', 'r', encoding="utf8")
    videolections = []
    for line in f:
        try:
            data = line.split('~')
            data[1] = data[1].replace("\n", "")
            videolections.append(
                {
                    'link': data[0],
                    'name': data[1]
                }
            )
        except Exception as e:
            pass
    f.close()
    return videolections


def spisok(message, text):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    programm = result["programm"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    videolections = get_videolections()
    for i in videolections:
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
            reply_markup=keyboard_video
        )
    else:
        flag = True
        videolections = get_videolections()
        for i in videolections:
            if i['name'] == message.text:
                spisok(message, i['link'])
                flag = False
                break
        if flag:
            bot.send_message(
                message.from_user.id,
                "Такого видео нет",
                reply_markup=keyboard_video
            )
