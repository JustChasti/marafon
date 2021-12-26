from os import remove
from threading import Thread
from loguru import logger
from telebot import *
from db.db import user_collection
from config import bot

from modules import registration

from modules.keyboards import keyboard_mind, keyboard_health, keyboard_main, keyboard_stats_b, keyboard_other
from modules.statistic.stats import get_beginer_week, get_beginer_stats, get_3program_stats, get_all_stats, my_stats

from modules.tasks.shichko import shichko
from modules.tasks.thanks import thanks
from modules.tasks.plans import plans
from modules.tasks.lessons import stream
from modules.tasks.book import book
from modules.tasks.audio_book import audio_book
from modules.tasks.clean_day import register_clean
from modules.tasks.fitness_game import game
from modules.tasks.sport import sport
from modules.tasks.jogging import run_walk

from modules.reminder.fileworker import main_tasks_worker

from modules.admin.admin import chek_password

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
        bot.register_next_step_handler(message, registration.registration)


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
    except TypeError as e:
        logger.exception(e)


try:
    main_tasks_thread = Thread(target=main_tasks_worker)
    main_tasks_thread.start()
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception(e)
