from os import remove
from datetime import date, datetime
from loguru import logger
from telebot import types
from db.db import user_collection
from db.db import main_collection, run_walk_collection, sport_collection, books_collection, plans_collection, thanks_collection, shichko_collection
from config import bot
from modules.keyboards import keyboard_admin
import openpyxl


excel_path = 'modules/excel/data/stats.xlsx'


def collectoin_out(message, collection, c_name):
    bot.send_message(
        message.from_user.id,
        c_name,
    )
    for i in collection:
        if '.jpg' in i['data']:
            img = open(i['data'], 'rb')
            bot.send_photo(
                message.from_user.id,
                img,
            )
            img.close()
        else:
            bot.send_message(
                message.from_user.id,
                i['data'],
            )


def table_to_excel(message, collection, c_name, admin_panel):
    data = collection.find({})
    wb = openpyxl.load_workbook(filename=excel_path)
    sheet = wb.active
    sheet.title = c_name
    sheet[f'A1'] = "Пользователь"
    sheet[f'B1'] = "Текст или адрес фото"
    sheet[f'C1'] = "Дата"
    counter = 2
    for i in data:
        sheet[f'A{counter}'] = i["user"]
        sheet[f'B{counter}'] = i["data"]
        sheet[f'C{counter}'] = i["date"]
        counter += 1
    wb.save(f'modules/excel/data/{c_name}.xlsx')
    doc = open(f'modules/excel/data/{c_name}.xlsx', 'rb')
    bot.send_document(
        message.from_user.id,
        doc,
        reply_markup=keyboard_admin
    )
    doc.close()
    remove(f'modules/excel/data/{c_name}.xlsx')
    bot.register_next_step_handler(message, admin_panel)


def get_tasks_user(message, name, admin_panel):
    try:
        user = user_collection.find_one({'name': name})
        if user:
            data = main_collection.find({'user': name})
            collectoin_out(message, data, 'основные')

            data = run_walk_collection.find({'user': name})
            collectoin_out(message, data, 'пробежка прогулка')

            data = sport_collection.find({'user': name})
            collectoin_out(message, data, 'тренировка')

            data = books_collection.find({'user': name})
            collectoin_out(message, data, 'книги')

            data = plans_collection.find({'user': name})
            collectoin_out(message, data, 'планирование')

            data = thanks_collection.find({'user': name})
            collectoin_out(message, data, 'благодарности')

            data = shichko_collection.find({'user': name})
            collectoin_out(message, data, 'шичко')
        else:
            bot.send_message(
                message.from_user.id,
                'такого пользователя нет',
            )
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
        )

    bot.send_message(
        message.from_user.id,
        "Вывел все задания что были",
        reply_markup=keyboard_admin
    )
    bot.register_next_step_handler(message, admin_panel)


def get_tasks_table(message, name, admin_panel):
    try:
        task_dict = {
            'Шичко': shichko_collection,
            'Благодарности': thanks_collection,
            'Планирование': plans_collection,
            'Книги': books_collection,
            'Тренировки': sport_collection,
            'Пробежки': run_walk_collection,
            'Основные': main_collection,
        }
        # table_to_excel(message, task_dict[name], name, admin_panel)
        data = task_dict[name].find({})
        bot.send_message(
            message.from_user.id,
            "Введите период например (01.01.22-02.02.22)",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, period_handler, data, admin_panel)
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            'Такой таблицы нет',
            reply_markup=keyboard_admin
        )
        bot.register_next_step_handler(message, admin_panel)


def period_handler(message, task, admin_panel):
    try:
        data = message.text.split('-')
        begin = datetime.strptime(data[0], '%d.%m.%y').date()
        end = datetime.strptime(data[1], '%d.%m.%y').date()
        for i in task:
            try:
                task_date = datetime.strptime(i['date'], '%Y-%m-%d').date()
                if task_date >= begin and task_date <= end:
                    if 'user-data' in i['data']:
                        img = open(i['data'], 'rb')
                        bot.send_photo(
                            message.from_user.id,
                            img,
                            reply_markup=keyboard_admin
                        )
                        img.close()
                    else:
                        bot.send_message(
                            message.from_user.id,
                            i['data'],
                            reply_markup=keyboard_admin
                        )
                        bot.register_next_step_handler(message, admin_panel)
            except Exception as e:
                logger.exception(e)
    except Exception as e:
        bot.send_message(
            message.from_user.id,
            'Ошибка в периоде',
            reply_markup=keyboard_admin
        )
        logger.exception(e)
        bot.register_next_step_handler(message, admin_panel)
