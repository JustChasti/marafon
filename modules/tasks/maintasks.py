import os
from telebot import types
from datetime import date, datetime
from db.db import user_collection, main_collection
from config import bot, regular_tasks


@bot.callback_query_handler(func=lambda c: c.data[:3] == 'mt/')
def main_tasks(callback_query: types.CallbackQuery):
    task_id = callback_query.data[3:]
    msg = bot.send_message(callback_query.message.chat.id,
                           "Напишите ответ или загрузите в виде фото"
                           )
    bot.register_next_step_handler(msg, m_tasks, task_id)


def update_main_tasks(data, user_name):
    result = main_collection.find_one(
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
        main_collection.insert_one(element)
        return True


def m_tasks(message, task_data):
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    path = f'user-data/{message.from_user.id}'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Запрограммированность')
    button2 = types.KeyboardButton('Задания по лекциям')
    button3 = types.KeyboardButton('Дополнительные задания')
    button4 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3, button4)
    result = user_collection.find_one({'telegram_id': message.from_user.id})

    task_id, task_score = task_data.split(".")
    task_id, task_score = int(task_id), int(task_score)

    if result["programm"] == "beginer":
        delta = date.today() - start_date
        delta = int(delta.days)
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            name = f'{path}/{date.today()}-задание {task_id}.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_main_tasks(name, result["name"])
        else:
            data = message.text
            response = update_main_tasks(data, result["name"])

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
                data = result[week]
                data["main_tasks"] += task_score
                element = {
                    "$set": {
                        week: data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                data_week = regular_tasks
                data_week['main_tasks'] = task_score
                element = {
                    "$set": {
                        week: data_week
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Задание загружено",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня основное задание",
                             reply_markup=keyboard
                             )

    else:
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            name = f'{path}/{date.today()}-задание {task_id}.jpg'
            try:
                with open(name, 'wb') as out:
                    out.write(data)
            except Exception as e:
                os.makedirs(str(path))
                with open(name, 'wb') as out:
                    out.write(data)
            response = update_main_tasks(name, result["name"])
        else:
            data = message.text
            response = update_main_tasks(data, result["name"])

        if response:
            try:
                data = result['main_tasks'] + task_score
                element = {
                    "$set": {
                        'main_tasks': data
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            except KeyError as e:
                element = {
                    "$set": {
                        'main_tasks': task_score
                    }
                }
                user_collection.update_one({'_id': result["_id"]}, element)
            bot.send_message(message.from_user.id,
                             "Задание загружено",
                             reply_markup=keyboard
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Вы уже делали сегодня основное задание",
                             reply_markup=keyboard
                             )
