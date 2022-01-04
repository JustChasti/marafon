from os import remove
from datetime import date
from loguru import logger
from db.db import user_collection
from config import bot
from config import start_date
from modules.keyboards import keyboard_admin
import openpyxl
from  modules.excel import converter


def add_to_user(message, data, admin_panel):
    try:
        name,mark = data.split('/')
        user = user_collection.find_one({'name': name})
        try:
            data = user['critical'] + int(mark)
            element = {
                "$set": {
                    'critical': data
                }
            }
            user_collection.update_one({'_id': user["_id"]}, element)
        except Exception as e:
            element = {
                "$set": {
                    'critical': int(mark)
                }
            }
            user_collection.update_one({'_id': user["_id"]}, element)
        bot.send_message(
            message.from_user.id,
            'Добавлено',
            reply_markup=keyboard_admin
        )
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


excel_path = 'modules/excel/data/stats0.xlsx'


def get_beginer_week_table(message, data, admin_panel):
    try:
        delta = date.today() - start_date
        delta = int(delta.days)
        if delta < 7:
            week = 'week 1'
        elif delta < 14:
            week = 'week 2'
        elif delta < 21:
            week = 'week 3'
        else:
            week = 'week 4'
        try:
            users = user_collection.find({'programm': 'beginer'})
            row = 2
            wb = openpyxl.load_workbook(filename=excel_path)
            sheet = wb.active
            sheet.title = 'Статистика'
            sheet[f'A1'] = 'Имя'
            sheet[f'B1'] = 'Шичко'
            sheet[f'C1'] = 'Планирование'
            sheet[f'D1'] = 'Благодарности'
            sheet[f'E1'] = 'Основные'
            sheet[f'F1'] = 'Книга'
            sheet[f'G1'] = 'Аудио книга'
            sheet[f'H1'] = 'Спорт'
            sheet[f'I1'] = 'Фитнес игра'
            sheet[f'J1'] = 'Пробежки прогулки'
            sheet[f'K1'] = 'Чистые дни'
            sheet[f'L1'] = 'Прямой эфир'
            sheet[f'M1'] = 'Общий балл'
            for i in users:
                data = i[week]
                sum = 0
                sheet[f'A{row}'] = i["name"]
                column = 'B'
                print(data)
                for j in data:
                    sum += int(data[j])
                    sheet[f'{column}{row}'] = data[j]
                    column = chr(ord(column) + 1)
                sheet[f'{column}{row}'] = sum
                row += 1
            wb.save('modules/excel/data/begins_stat.xlsx')

        except Exception as e:
            logger.exception(e)


        doc = open('modules/excel/data/begins_stat.xlsx', 'rb')
        bot.send_document(message.from_user.id,
                            doc,
                            reply_markup=keyboard_admin
                            )
        doc.close()
        remove('modules/excel/data/begins_stat.xlsx')
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


class table_does_not_exist(Exception):
   pass


def get_potok_table(message, data, admin_panel):
    try:
        if data == 'Старт':
            programm = 'start'
        elif data == 'Лидер':
            programm = 'leader'
        elif data == 'Эксперт':
            programm = 'profi'
        else:
            raise table_does_not_exist('Такой таблицы нет')

        users = user_collection.find({'programm': programm})
        row = 2
        wb = openpyxl.load_workbook(filename=excel_path)
        sheet = wb.active
        sheet.title = 'Статистика'
        sheet[f'A1'] = 'Имя'
        sheet[f'B1'] = 'Шичко'
        sheet[f'C1'] = 'Планирование'
        sheet[f'D1'] = 'Благодарности'
        sheet[f'E1'] = 'Основные'
        sheet[f'F1'] = 'Книга'
        sheet[f'G1'] = 'Аудио книга'
        sheet[f'H1'] = 'Спорт'
        sheet[f'I1'] = 'Фитнес игра'
        sheet[f'J1'] = 'Пробежки прогулки'
        sheet[f'K1'] = 'Чистые дни'
        sheet[f'L1'] = 'Прямой эфир'
        sheet[f'M1'] = 'Добавочные'
        sheet[f'N1'] = 'Общий балл'
        for i in users:
            sum = 0
            sheet[f'A{row}'] = i["name"]
            try:
                sum += int(i['shichko'])
                sheet[f'B{row}'] = i['shichko']
            except Exception as e:
                sheet[f'B{row}'] = 0
            try:
                sum += int(i['plans'])
                sheet[f'C{row}'] = i['plans']
            except Exception as e:
                sheet[f'C{row}'] = 0
            try:
                sum += int(i['thanks'])
                sheet[f'D{row}'] = i['thanks']
            except Exception as e:
                sheet[f'D{row}'] = 0
            try:
                sum += int(i['main_task'])
                sheet[f'E{row}'] = i['main_task']
            except Exception as e:
                sheet[f'E{row}'] = 0
            try:
                sum += int(i['book'])
                sheet[f'F{row}'] = i['book']
            except Exception as e:
                sheet[f'F{row}'] = 0
            try:
                sum += int(i['audio_book'])
                sheet[f'G{row}'] = i['audio_book']
            except Exception as e:
                sheet[f'G{row}'] = 0
            try:
                sum += int(i['sport'])
                sheet[f'H{row}'] = i['sport']
            except Exception as e:
                sheet[f'H{row}'] = 0
            try:
                sum += int(i['fitness-game'])
                sheet[f'I{row}'] = i['fitness-game']
            except Exception as e:
                sheet[f'I{row}'] = 0
            try:
                sum += int(i['run-walk'])
                sheet[f'J{row}'] = i['run-walk']
            except Exception as e:
                sheet[f'J{row}'] = 0
            try:
                sum += int(i['clean'])
                sheet[f'K{row}'] = i['clean']
            except Exception as e:
                sheet[f'K{row}'] = 0
            try:
                sum += int(i['stream'])
                sheet[f'L{row}'] = i['stream']
            except Exception as e:
                sheet[f'L{row}'] = 0
            try:
                sum += int(i['critical'])
                sheet[f'M{row}'] = i['critical']
            except Exception as e:
                sheet[f'M{row}'] = 0

            sheet[f'N{row}'] = sum
            row += 1
        wb.save('modules/excel/data/begins_stat.xlsx')


        doc = open('modules/excel/data/begins_stat.xlsx', 'rb')
        bot.send_document(message.from_user.id,
                            doc,
                            reply_markup=keyboard_admin
                            )
        doc.close()
        remove('modules/excel/data/begins_stat.xlsx')
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


def get_all_table(message, data, admin_panel):
    try:
        users = user_collection.find({})
        row = 2
        wb = openpyxl.load_workbook(filename=excel_path)
        sheet = wb.active
        sheet.title = 'Статистика'
        sheet[f'A1'] = 'Имя'
        sheet[f'B1'] = 'Этап"'
        sheet[f'C1'] = 'Балл'
        for i in users:
            sum = 0
            try:
                if i['programm'] == 'beginer':
                    try:
                        sum += i['critical']
                    except Exception as e:
                        pass
                    for j in i:
                        if 'week' in j:
                            data = i[j]
                            for k in data:
                                sum += int(data[k])
                else:
                    for j in i:
                        if j != 'telegram_id':
                            try:
                                sum += int(i[j])
                            except Exception as e:
                                pass
            except Exception as e:
                logger.info('user not registred')

            sheet[f'A{row}'] = i['name']
            sheet[f'B{row}'] = i['stage']
            sheet[f'C{row}'] = sum
            row += 1


        wb.save('modules/excel/data/begins_stat.xlsx')

        doc = open('modules/excel/data/begins_stat.xlsx', 'rb')
        bot.send_document(message.from_user.id,
                            doc,
                            reply_markup=keyboard_admin
                            )
        doc.close()
        remove('modules/excel/data/begins_stat.xlsx')
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


def up_potok_main(message, admin_panel):
    try:
        fileID = message.document.file_id
        file_info = bot.get_file(fileID)
        data = bot.download_file(file_info.file_path)
        name = f'modules/reminder/data/{message.document.file_name}'
        with open(name, 'wb') as out:
                out.write(data)
        bot.send_message(
            message.from_user.id,
            f'загружен файл {name}',
            reply_markup=keyboard_admin
        )
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


def up_to_excel(message, admin_panel):
    try:
        fileID = message.document.file_id
        file_info = bot.get_file(fileID)
        data = bot.download_file(file_info.file_path)
        name = f'modules/excel/data/{message.document.file_name}'
        with open(name, 'wb') as out:
                out.write(data)
        converter.excel_to_mongo(name)
        bot.send_message(
            message.from_user.id,
            f'загружен файл {name}',
            reply_markup=keyboard_admin
        )
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)


def send_to_potok(message, data, admin_panel):
    try:
        if data == 'Новичок':
            programm = 'beginer'
        elif data == 'Старт':
            programm = 'start'
        elif data == 'Лидер':
            programm = 'leader'
        elif data == 'Эксперт':
            programm = 'profi'
        else:
            raise table_does_not_exist('Такой таблицы нет')
        users = user_collection.find({'programm': programm})
        for i in users:
            try:
                bot.send_message(
                    i["telegram_id"],
                    message.text,
                )
            except Exception as e:
                logger.exception(e)
                bot.send_message(
                    message.from_user.id,
                    f'Пользователь {i["name"]} не зарегистрирован или вы отправляете не текст',
                    reply_markup=keyboard_admin
                )
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.send_message(
        message.from_user.id,
        message.text,
        reply_markup=keyboard_admin
    )
    bot.register_next_step_handler(message, admin_panel)


def get_photo_by_data(message, data, admin_panel):
    try:
        img = open(data, 'rb')
        bot.send_photo(
            message.from_user.id,
            img,
            reply_markup=keyboard_admin
        )
        img.close()
    except Exception as e:
        logger.exception(e)
        bot.send_message(
            message.from_user.id,
            str(e),
            reply_markup=keyboard_admin
        )
    bot.register_next_step_handler(message, admin_panel)
