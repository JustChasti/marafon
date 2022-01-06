import os
from telebot import types
from datetime import date
from db.db import user_collection, main_collection
from config import bot, start_date, begin_main, start_main, leader_main, expert_main, regular_tasks
from modules.keyboards import keyboard_mind


def spisok(message, text):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    programm = result["programm"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if programm == 'beginer':
        data = begin_main
    elif programm == 'start':
        data = start_main
    elif programm == 'leader':
        data = leader_main
    elif programm == 'profi':
        data = expert_main
    for i in data:
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
    bot.register_next_step_handler(message, switch)


def handler(message, name):
    ball = 0
    if message.text == 'Назад':
        spisok(message,'Выберете вариант')
    else:
        result = user_collection.find_one({'telegram_id': message.from_user.id})
        programm = result["programm"]
        if programm == 'beginer':
            data = begin_main
        elif programm == 'start':
            data = start_main
        elif programm == 'leader':
            data = leader_main
        elif programm == 'profi':
            data = expert_main
        for i in data:
            if i['name'] == name:
                ball = i['score']
                break
        m_tasks(message, name, ball)


def update_main_tasks(data, user_name):
    element = {
        'user': user_name,
        'date': str(date.today()),
        'data': data

    }
    main_collection.insert_one(element)
    return True


def m_tasks(message, task_name, task_score):
    path = f'user-data/{message.from_user.id}'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Мышление')
    button2 = types.KeyboardButton('Здоровье')
    button3 = types.KeyboardButton('Статистика')
    keyboard.add(button1, button2, button3)
    result = user_collection.find_one({'telegram_id': message.from_user.id})

    if result["programm"] == "beginer":
        delta = date.today() - start_date
        delta = int(delta.days)
        if message.photo:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            data = bot.download_file(file_info.file_path)
            name = f'{path}/{date.today()}-задание {task_name}.jpg'
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
            name = f'{path}/{date.today()}-задание {task_name}.jpg'
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


def switch(message):
    if message.text == 'Назад':
        bot.send_message(
            message.from_user.id,
            "Назад",
            reply_markup=keyboard_mind
        )
    else:
        bot.send_message(
            message.from_user.id,
            "Напишите задание текстом или отправьте фото",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, handler, message.text)
