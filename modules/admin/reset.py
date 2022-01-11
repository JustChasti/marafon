import os
import shutil
from datetime import date,  datetime
import threading
from config import bot
from config import start_date
from modules.keyboards import keyboard_admin
from loguru import logger
from db import db
from modules.reminder.fileworker import work_flag, main_tasks_worker
import time


def reset_config(message, data, admin_panel):
    try:
        start_date = datetime.strptime(data, '%d.%m.%Y').date()
        shutil.rmtree('user-data')
        os.mkdir('user-data')
        bot.send_message(
                message.from_user.id,
                "Данные сброшены, новый поток сообщений будет запущен через 24 часа",
                reply_markup=keyboard_admin
            )
        db.user_collection.drop()
        db.thanks_collection.drop()
        db.plans_collection.drop({})
        db.books_collection.drop({})
        db.user_collection.drop({})
        db.lessons_collection.drop({})
        db.clean_collection.drop({})
        db.sport_collection.drop({})
        db.run_walk_collection.drop({})
        db.user_collection.drop({})
        db.main_collection.drop({})
        db.shichko_collection = db.db["shichko"]
        db.thanks_collection = db.db["thanks"]
        db.plans_collection = db.db["plans"]
        db.books_collection = db.db["books"]
        db.lessons_collection = db.db["lessons"]
        db.clean_collection = db.db["clean"]
        db.sport_collection = db.db["sport"]
        db.run_walk_collection = db.db["run_walk"]
        db.user_collection = db.db["user"]
        db.main_collection = db.db["main"]
        f = open('modules/reminder/data/data.txt', 'w', encoding="utf8")
        f.write("0")
        f.close()
        help = threading.Thread(target=mesage_starter)
        help.start()
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


def mesage_starter():
    logger.info('Запущен еще один поток, который запустит сообщения')
    time.sleep(60*60*24)
    main_tasks_thread = threading.Thread(target=main_tasks_worker)
    main_tasks_thread.start()
