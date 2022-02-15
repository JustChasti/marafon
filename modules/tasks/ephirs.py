from telebot import types
from datetime import date, datetime
from db.db import user_collection, clean_collection
from config import bot, scores
from modules.keyboards import keyboard_mind, keyboard_mind
from datetime import datetime


def get_ephirs():
    f = open('modules/reminder/data/ephirs.txt', 'r', encoding="utf8")
    ephirs = []
    for line in f:
        try:
            data = line.split('~')
            data[3] = data[3].replace("\n", "")
            ephirs.append(
                {
                    'link': data[0],
                    'name': data[1],
                    'date':  datetime.strptime(data[2], '%d.%m.%y').date(),
                    'etap': data[3]
                }
            )
        except Exception as e:
            print(e)
    f.close()
    return ephirs


def spisok(message, text):
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    programm = result["programm"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ephirs = get_ephirs()
    for i in ephirs:
        if (i['etap'] == programm or i['etap'] == 'all') and i['date'] <= date.today():
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
        ephirs = get_ephirs()
        for i in ephirs:
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
