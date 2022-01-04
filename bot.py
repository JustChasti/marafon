from os import name
from datetime import date
from threading import Thread
from loguru import logger
from telebot import *
from db.db import user_collection
from config import bot

from keyboards import keyboard_mind, keyboard_health, keyboard_main, keyboard_stats_b, keyboard_other, keyboard_programs, keyboard_switch
from db.stats import get_beginer_week, get_beginer_stats, get_3program_stats, get_all_stats

from tasks import shichko
from tasks import thanks
from tasks import plans
from tasks import lessons
from tasks import book
from tasks import audio_book
from tasks import clean_day
from tasks.fitness_game import game
from tasks.sport import sport
from tasks.jogging import run_walk

from tasks.maintasks import m_tasks
from fileworker import main_tasks_worker
from excel import converter


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
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, shichko.menu)

    elif message.text == 'Благодарности':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, thanks.menu)

    elif message.text == 'Планирование':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, plans.menu)

    elif message.text == 'Посещение прямых эфиров':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, lessons.menu)

    elif message.text == 'Книга':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, book.menu)

    elif message.text == 'Аудио-книга':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, audio_book.menu)

    elif message.text == 'Зарегистрировать чистый день':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, clean_day.menu)

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
    elif message.text == 'За все среди текущего этапа':
        result = get_3program_stats(message.from_user.id)
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )
    elif message.text == 'Среди всех этапов':
        result = get_all_stats()
        bot.send_message(message.from_user.id,
                         result,
                         reply_markup=keyboard_main
                         )

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


try:
    # converter.excel_to_mongo("input.xlsx")
    # main_tasks_thread = Thread(target=main_tasks_worker)
    # main_tasks_thread.start()
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception(e)
