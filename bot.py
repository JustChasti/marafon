from os import remove
from threading import Thread
from loguru import logger
import loguru
from telebot import *
from db.db import user_collection
from config import bot
from datetime import date, datetime

from modules import registration

from modules.keyboards import keyboard_mind, keyboard_health, keyboard_main
from modules.keyboards import keyboard_stats_b, keyboard_other, keyboard_switch
from modules.keyboards import keyboard_fit_game
from modules.statistic.stats import get_beginer_week, get_beginer_stats
from modules.statistic.stats import get_3program_stats, get_all_stats, my_stats

from modules.tasks import shichko
from modules.tasks import thanks
from modules.tasks import plans
from modules.tasks import lessons
from modules.tasks import book
from modules.tasks import audio_book
from modules.tasks import clean_day
from modules.tasks import videolections, ephirs
from modules.tasks import shower
from modules.tasks import maint

from modules.tasks import fitness_game
from modules.tasks.sport import sport
from modules.tasks.jogging import run_walk

from modules.reminder.fileworker import main_tasks_worker

from modules.admin.admin import chek_password

from try_wrapper import try_wrapper


@bot.message_handler(commands=['help', 'start'])
@try_wrapper
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
        bot.register_next_step_handler(message, registration.registration)


@bot.message_handler(commands=['admin'])
@try_wrapper
def start_chat(message):
    bot.send_message(message.from_user.id,
                     "Введите пароль"
                     )
    bot.register_next_step_handler(message, chek_password)


@bot.message_handler(content_types=['text'])
@try_wrapper
def main_chat(message):
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    print(f'{start_date}')
    result = user_collection.find_one({'telegram_id': message.from_user.id})
    if not result or datetime.now().date() < start_date:
        bot.send_message(message.from_user.id,
                         "Вы незарегистрированы или поток еще не стартовал"
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

    elif message.text == 'Контрастный душ':
        bot.send_message(message.from_user.id,
                         "Выберете варинт",
                         reply_markup=keyboard_switch
                         )
        bot.register_next_step_handler(message, shower.menu)

    elif message.text == 'Видеолекции':
        videolections.spisok(message, 'Выберите вариант')

    elif message.text == 'Эфиры':
        ephirs.spisok(message, 'Выберите вариант')

    elif message.text == 'Основные':
        maint.spisok(message, 'Выберите вариант')

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
                         "Выберите уровень",
                         reply_markup=keyboard_fit_game
                         )
        bot.register_next_step_handler(message, fitness_game.game_switch)

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

    elif message.text == 'Моя статистика':
        result = my_stats(message.from_user.id)
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
@try_wrapper
def sport_photo(message):
    f = open('modules/reminder/data/start_date.txt', 'r', encoding="utf8")
    for i in f:
        s_date = i
        break
    start_date = datetime.strptime(s_date, '%d.%m.%Y').date()
    try:
        if '#тренировка' in message.caption or '#Тренировка' in message.caption:
            result = user_collection.find_one({'telegram_id': message.from_user.id})
            if not result or datetime.now().date() < start_date:
                bot.send_message(
                    message.from_user.id,
                    "Вы незарегистрированы или поток еще не стартовал"
                )
            else:
                sport(message)
        elif '#пробежка' in message.caption or '#Пробежка' in message.caption:
            result = user_collection.find_one({'telegram_id': message.from_user.id})
            if not result or datetime.now().date() < start_date:
                bot.send_message(
                    message.from_user.id,
                    "Вы незарегистрированы или поток еще не стартовал"
                )
            else:
                run_walk(message, True)
        elif '#прогулка' in message.caption or '#Прогулка' in message.caption:
            result = user_collection.find_one({'telegram_id': message.from_user.id})
            if not result or datetime.now().date() < start_date:
                bot.send_message(
                    message.from_user.id,
                    "Вы незарегистрированы или поток еще не стартовал"
                )
            else:
                run_walk(message, False)
    except TypeError as e:
        logger.exception(e)


try:
    loguru.logger.add("marafon.log", rotation="200 MB")
    main_tasks_thread = Thread(target=main_tasks_worker)
    main_tasks_thread.start()
    while True:
        try:
            logger.info('bot started')
            bot.polling(none_stop=True)
        except Exception as e:
            logger.exception(e)
except Exception as e:
    logger.exception(e)
