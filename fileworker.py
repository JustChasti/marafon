from datetime import datetime, timedelta
from datetime import time as ddtime
import time
from loguru import logger
from telebot import *
from config import bot, main_hours
from db.db import user_collection


def main_tasks_worker():
    counter = 0
    main_tasks_time = ddtime(main_hours)
    while True:
        users = user_collection.find({})
        if datetime.now().time().hour == main_tasks_time.hour:
            for i in users:
                task = 0
                try:
                    if i["programm"] == "beginer":
                        f = open('tasks/beginer_tasks.txt', 'r', encoding="utf8")
                    elif i["programm"] == "start":
                        f = open('tasks/start_tasks.txt', 'r', encoding="utf8")
                    elif i["programm"] == "profi":
                        f = open('tasks/expert_tasks.txt', 'r', encoding="utf8")
                    elif i["programm"] == "leader":
                        f = open('tasks/leader_tasks.txt', 'r', encoding="utf8")
                    s = ''
                    for line in f:
                        if '~' in line:
                            if task == counter:
                                tail = line[1:]
                                if s in tail:
                                    keyboard = types.InlineKeyboardMarkup()
                                    button1 = types.InlineKeyboardButton('Сдать задание', callback_data=f"mt/{counter}.{line[1:]}")
                                    keyboard.add(button1)
                                    bot.send_message(i["telegram_id"], s, reply_markup=keyboard)
                                else:
                                    bot.send_message(i["telegram_id"], s)
                            elif task > counter:
                                break
                            s = ''
                            task += 1
                        else:
                            s += line
                except Exception as e:
                    logger.exception(e)
            counter += 1
            time.sleep(70000)
        else:
            if datetime.now().time() < main_tasks_time:
                push = datetime.now()
                push = push.replace(hour=main_hours, minute=0, second=0, microsecond=0)
                delta = push - datetime.now()
            else:
                push = datetime.now()
                push = push.replace(hour=main_hours, minute=0, second=0, microsecond=0)
                push += timedelta(days=1)
                delta = push - datetime.now()
            print(delta.seconds)
            time.sleep(delta.seconds)


def main_tasks_test():
    counter = 0
    users = user_collection.find({})
    print(users)
    for i in users:
        task = 0
        try:
            if i["programm"] == "beginer":
                f = open('tasks/beginer_tasks.txt', 'r', encoding="utf8")
            elif i["programm"] == "start":
                f = open('tasks/start_tasks.txt', 'r', encoding="utf8")
            elif i["programm"] == "profi":
                f = open('tasks/expert_tasks.txt', 'r', encoding="utf8")
            elif i["programm"] == "leader":
                f = open('tasks/leader_tasks.txt', 'r', encoding="utf8")
            s = ''
            for line in f:
                if '~' in line:
                    print(line)
                    if task == counter:
                        tail = line[1:]
                        print(tail)
                        if s in tail:
                            print(1)
                            keyboard = types.InlineKeyboardMarkup()
                            button1 = types.InlineKeyboardButton('Сдать задание', callback_data=f"mt/{counter}.{line[1:]}")
                            keyboard.add(button1)
                            bot.send_message(i["telegram_id"], s, reply_markup=keyboard)
                        else:
                            print(2)
                            bot.send_message(i["telegram_id"], s)
                    elif task > counter:
                        break
                    s = ''
                    task += 1
                else:
                    s += line
        except Exception as e:
            logger.exception(e)


if __name__ == "__main__":
    main_tasks_test()
