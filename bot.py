from os import name, path, remove
from datetime import date
from threading import Thread
from loguru import logger
from telebot import *
from db.db import user_collection
from config import bot, admin_password

from keyboards import keyboard_mind, keyboard_health, keyboard_main, keyboard_stats_b, keyboard_other, keyboard_programs, keyboard_admin
from db.stats import get_beginer_week, get_beginer_stats, get_3program_stats, get_all_stats, my_stats

from tasks.shichko import shichko
from tasks.thanks import thanks
from tasks.plans import plans
from tasks.lessons import stream
from tasks.book import book
from tasks.audio_book import audio_book
from tasks.clean_day import register_clean
from tasks.fitness_game import game
from tasks.sport import sport
from tasks.jogging import run_walk

from tasks.maintasks import m_tasks
from fileworker import main_tasks_worker
from excel import converter

from admin.tasks import get_tasks_user, get_tasks_table
from admin.users import add_to_user, get_beginer_week_table, get_potok_table, get_beginer_week_table, get_all_table, up_potok_main, up_to_excel, send_to_potok, get_photo_by_data


@bot.message_handler(commands=['help', 'start'])
def start_chat(message):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if result:
        bot.send_message(message.from_user.id,
                         "Вы уже зарегестрированы - работайте по программе"
                         )
    else:
        bot.send_message(message.from_user.id,
                         "Введите ваше имя"
                         )
        bot.register_next_step_handler(message, registration)


@bot.message_handler(commands=['admin'])
def start_chat(message):
    bot.send_message(message.from_user.id,
                     "Введите пароль"
                     )
    bot.register_next_step_handler(message, chek_password)


@bot.message_handler(content_types=['text'])
def main_chat(message):
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if not result:
        bot.send_message(message.from_user.id,
                         "Вы незарегистрированы"
                         )
    elif message.text == 'Мышление':
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_mind
                         )

    elif message.text == 'Здоровье':
        bot.send_message(message.from_user.id,
                         "Выбери задание",
                         reply_markup=keyboard_health
                         )

    elif message.text == 'Шичко':
        bot.send_message(message.from_user.id,
                         "Загрузите Шичко",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, shichko)

    elif message.text == 'Благодарности':
        bot.send_message(message.from_user.id,
                         "Напишите благодарности",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, thanks)

    elif message.text == 'Планирование':
        bot.send_message(message.from_user.id,
                         "Напишите планирование",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, plans)

    elif message.text == 'Посещение прямых эфиров':
        stream(message)

    elif message.text == 'Книга':
        bot.send_message(message.from_user.id,
                         "Напишите название книги",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, book)

    elif message.text == 'Аудио-книга':
        bot.send_message(message.from_user.id,
                         "Напишите название книги",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, audio_book)

    elif message.text == 'Зарегистрировать чистый день':
        register_clean(message)

    elif message.text == 'Фитнес игра':
        bot.send_message(message.from_user.id,
                         "Напишите балл за фитнес игру (ТОЛЬКО ЧИСЛО)",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        bot.register_next_step_handler(message, game)

    elif '#тренировка' in message.text or '#Тренировка' in message.text:
        sport(message)

    elif '#пробежка' in message.text or '#Пробежка' in message.text:
        run_walk(message, True)

    elif '#прогулка' in message.text or '#Прогулка' in message.text:
        run_walk(message, False)

    elif message.text == 'Назад':
        bot.send_message(message.from_user.id,
                         "Назад",
                         reply_markup=keyboard_main
                         )
    elif message.text == 'Статистика':
        if result['programm'] == 'beginer':
            bot.send_message(message.from_user.id,
                             "Выбери статистику",
                             reply_markup=keyboard_stats_b
                             )
        else:
            bot.send_message(message.from_user.id,
                             "Выбери статистику",
                             reply_markup=keyboard_other
                             )

    elif message.text == 'Текущая неделя среди новичков':
        result = get_beginer_week()
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )
    elif message.text == 'За все время среди новичков':
        result = get_beginer_stats()
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )
    elif message.text == 'За все среди текущего потока':
        result = get_3program_stats(message.from_user.id)
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )
    elif message.text == 'Среди всех потоков':
        result = get_all_stats()
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )

    elif message.text == 'Моя статистика':
        result = my_stats(message.from_user.id)
        doc = open(result, 'rb')
        bot.send_document(message.from_user.id,
                         doc,
                         reply_markup=keyboard_main
                         )
        doc.close()
        remove(f'excel/{message.from_user.id}.xlsx')

    elif message.text == 'Вывод монги':
        users = user_collection.find({})
        for i in users:
            print(i)

    else:
        print(message.text)


@bot.message_handler(content_types=['photo'])
def sport_photo(message):
    try:
        if '#тренировка' in message.caption or '#Тренировка' in message.caption:
            sport(message)
        elif '#пробежка' in message.caption or '#Пробежка' in message.caption:
            run_walk(message, True)
        elif '#прогулка' in message.caption or '#Прогулка' in message.caption:
            run_walk(message, False)
    except TypeError:
        print(11111)


def registration(message):
    result = user_collection.find_one({'name': message.text})
    if result:
        element = {
            "$set": {
                'telegram_id': message.from_user.id
            }
        }
        user_collection.update_one({'name': message.text}, element)
        bot.send_message(message.from_user.id,
                         "Добро пожаловать на Марафон"
                         )
        bot.send_message(message.from_user.id,
                         "Теперь выбери свой этап. Если ты выпуснкик, то можешь выбрать любой из этапов",
                         reply_markup=keyboard_programs
                         )
    else:
        bot.send_message(message.from_user.id,
                         "Вы не доавлены в проект: Обратитесь к Никите(https://t.me/nixon49) или к разработчику (https://t.me/kot_gray)"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'beginer')
def process_callback_button1(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Новичок") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'beginer'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Новичок",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'starter')
def process_callback_button2(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Старт") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'start'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Старт",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'profi')
def process_callback_button3(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Эксперт") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'profi'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Эксперт",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data == 'leader')
def process_callback_button4(callback_query: types.CallbackQuery):
    result = user_collection.find_one({'telegram_id': callback_query.from_user.id})
    if (result["stage"] == "Лидер") or (result["stage"] == "Выпускник"):
        element = {
            "$set": {
                'programm': 'leader'
            }
        }
        user_collection.update_one({'telegram_id': callback_query.from_user.id}, element)
        bot.send_message(callback_query.from_user.id,
                         "Теперь вы работаете по программе Лидер",
                         reply_markup=keyboard_main
                         )
    else:
        bot.send_message(callback_query.from_user.id,
                         "Работа по этой программе вам недоступна"
                         )


@bot.callback_query_handler(func=lambda c: c.data[:3] == 'mt/')
def main_tasks(callback_query: types.CallbackQuery):
    task_id = callback_query.data[3:]
    msg = bot.send_message(callback_query.message.chat.id,
                           "Напишите ответ или загрузите в виде фото"
                           )
    bot.register_next_step_handler(msg, m_tasks, task_id)


def chek_password(message):
    try:
        if message.text == admin_password:
            bot.send_message(message.from_user.id,
                            "Пароль верен",
                            reply_markup=keyboard_admin
                            )
            bot.register_next_step_handler(message, admin_panel)
        else:
            bot.send_message(message.from_user.id,
                            "Неверный пароль"
                            )
    except Exception as e:
        logger.exception(e)


def admin_panel(message):
    keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Назад')
    keyboard_back.row(button)

    if message.text == 'Просмотр выполненных заданий пользователя ["X"]':
        bot.send_message(message.from_user.id,
                        "Введите Имя Город пользователя, например Григорий Москва",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, get_user_tasks)
    elif message.text == 'Просмотр таблицы заданий типа ["Y"]':
        bot.send_message(message.from_user.id,
                        "Введите название таблицы одно из ('Шичко', 'Благодарности', 'Планирование', 'Книги', 'Тренировки', 'Пробежки', 'Основные')",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, get_table_tasks)

    elif message.text == 'Добавить или отнять ["Y"] баллов у пользователя ["X"]':
        bot.send_message(message.from_user.id,
                        "Введите через символ '/' Имя Город/количество баллов Если нужно отнять баллы то просто ввести отрицательное количество",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, add_balls)
    elif message.text == 'Выгрузить таблицу текущей недели(у новичков)':
        get_beginer_week_table(message, message.text, admin_panel)

    elif message.text == 'Выгрузить таблицу потока ["X"]':
        bot.send_message(message.from_user.id,
                        "Введите название потока",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, get_x_table)

    elif message.text == 'Выгрузить общую таблицу среди всех потоков':
        get_all_table(message, message.text, admin_panel)

    elif message.text == 'Загрузить ежедневные задания для потока ["X"]':
        bot.send_message(message.from_user.id,
                        "Отправьте файл с задниями",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, up_main_tasks)
    elif message.text == 'Загрузить новую таблицу пользователей':
        bot.send_message(message.from_user.id,
                        "отправьте таблицу с заданиями",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, up_excel)

    elif message.text == 'Отправить сообщение для потока ["X"]':
        bot.send_message(message.from_user.id,
                        "Введите название потока",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, get_potok)
    
    elif message.text == 'Скачать фото':
        bot.send_message(message.from_user.id,
                        "Введите адрес фото из таблицы",
                        reply_markup=keyboard_back
                        )
        bot.register_next_step_handler(message, get_photo)

    else:
        bot.send_message(message.from_user.id,
                        message.text,
                        reply_markup=keyboard_back
                        )


def get_user_tasks(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        get_tasks_user(message, message.text, admin_panel)


def get_table_tasks(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        get_tasks_table(message, message.text, admin_panel)


def add_balls(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        add_to_user(message, message.text, admin_panel)


def get_x_table(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        get_potok_table(message, message.text, admin_panel)


def up_main_tasks(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        up_potok_main(message, admin_panel)


def up_excel(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        up_to_excel(message, admin_panel)


def get_potok(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        bot.send_message(message.from_user.id,
                        "Введите сообщение"
                        )
        bot.register_next_step_handler(message, send_to_potok, message.text, admin_panel)


def get_photo(message):
    if message.text == 'Назад':
        bot.send_message(message.from_user.id,
                        "Назад",
                        reply_markup=keyboard_admin
                        )
        bot.register_next_step_handler(message, admin_panel)
    else:
        get_photo_by_data(message, message.text, admin_panel)


try:
    # main_tasks_thread = Thread(target=main_tasks_worker)
    # main_tasks_thread.start()
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception(e)
