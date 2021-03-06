from datetime import datetime, timedelta
from datetime import time as ddtime
import time
from loguru import logger
from telebot import *
from config import bot, main_hours
from db.db import user_collection


work_flag = True


def main_tasks_worker():
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    counter = 0
    main_tasks_time = ddtime(main_hours)
    print('запущен Новая версия')
    while True:
        print('цикл начат')
        users = user_collection.find({})
        if datetime.now().time().hour == main_tasks_time.hour and datetime.now().date() >= start_date:
            print('1 ветка')
            try:
                for i in users:
                    task = 0
                    try:
                        if i["programm"] == "beginer":
                            f = open('modules/reminder/data/beginer_tasks.txt', 'r', encoding="utf8")
                        elif i["programm"] == "start":
                            f = open('modules/reminder/data/start_tasks.txt', 'r', encoding="utf8")
                        elif i["programm"] == "profi":
                            f = open('modules/reminder/data/expert_tasks.txt', 'r', encoding="utf8")
                        elif i["programm"] == "leader":
                            f = open('modules/reminder/data/leader_tasks.txt', 'r', encoding="utf8")
                        s = ''
                        for line in f:
                            if '~' in line:
                                if task == counter:
                                    bot.send_message(i["telegram_id"], s)
                                    """
                                    tail = line[1:]
                                    if s in tail:
                                        keyboard = types.InlineKeyboardMarkup()
                                        button1 = types.InlineKeyboardButton('Сдать задание', callback_data=f"mt/{counter}.{line[1:]}")
                                        keyboard.add(button1)
                                        bot.send_message(i["telegram_id"], s, reply_markup=keyboard)
                                    else:
                                        bot.send_message(i["telegram_id"], s)
                                    """
                                elif task > counter:
                                    break
                                s = ''
                                task += 1
                            else:
                                s += line
                    except Exception as e:
                        logger.exception(e)
                        print(e)
                counter += 1
                time.sleep(70000)
            except Exception as e:
                bot.send_message(362340468, str(e))
        else:
            print('2 ветка')
            logger.info(datetime.now().time().hour, datetime.now().date(), 'условие')
            print(datetime.now().time().hour, datetime.now().date(), 'условие')
            f = open('modules/reminder/data/data.txt', 'r', encoding="utf8")
            flag = False
            for i in f:
                if i == '0':
                    flag = True
            f.close()
            f = open('modules/reminder/data/data.txt', 'w', encoding="utf8")
            f.write("1")
            f.close()
            if flag:
                print('поток остановлен')
                break
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
            time.sleep(1)


if __name__ == "__main__":
    pass
