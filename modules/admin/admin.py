from telebot import *

from config import bot, admin_password
from modules.admin.tasks import get_tasks_user, get_tasks_table
from modules.admin.users import add_to_user, get_beginer_week_table, get_potok_table, get_beginer_week_table, get_all_table, up_potok_main, up_to_excel, send_to_potok
from modules.admin.reset import reset_config
from modules.keyboards import keyboard_admin


def default_wrapper(function):
    def wrapper(message):
        if message.text == 'Назад':
            bot.send_message(
                message.from_user.id,
                "Назад",
                reply_markup=keyboard_admin
            )
            bot.register_next_step_handler(message, admin_panel)
        else:
            function(message)
    return wrapper


def admin_panel(message):
    keyboard_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Назад')
    keyboard_back.row(button)

    if message.text == 'Просмотр выполненных заданий пользователя ["X"]':
        bot.send_message(
            message.from_user.id,
            "Введите Имя Город пользователя, например Григорий Москва",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, get_user_tasks)
    elif message.text == 'Просмотр таблицы заданий типа ["Y"]':
        bot.send_message(
            message.from_user.id,
            "Введите название таблицы одно из ('Шичко', 'Благодарности', 'Планирование', 'Книги', 'Тренировки', 'Пробежки', 'Основные')",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, get_table_tasks)

    elif message.text == 'Добавить или отнять ["Y"] баллов у пользователя ["X"]':
        bot.send_message(
            message.from_user.id,
            "Введите через символ '/' Имя Город/количество баллов Если нужно отнять баллы то просто ввести отрицательное количество",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, add_balls)
    elif message.text == 'Выгрузить таблицу текущей недели(у новичков)':
        get_beginer_week_table(message, message.text, admin_panel)

    elif message.text == 'Выгрузить таблицу потока ["X"]':
        bot.send_message(
            message.from_user.id,
            "Введите название потока",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, get_x_table)

    elif message.text == 'Выгрузить общую таблицу среди всех потоков':
        get_all_table(message, message.text, admin_panel)

    elif message.text == 'Загрузить файл':
        bot.send_message(
            message.from_user.id,
            "Отправьте файл с задниями",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, up_main_tasks)
    elif message.text == 'Добавить пользователей (Загрузка таблицы excel)':
        bot.send_message(
            message.from_user.id,
            "отправьте таблицу с заданиями",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, up_excel)

    elif message.text == 'Отправить сообщение для потока ["X"]':
        bot.send_message(
            message.from_user.id,
            "Введите название потока",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, get_potok)

    elif message.text == 'Очистить данные (перед запускам нового потока)':
        bot.send_message(
            message.from_user.id,
            "Вы уверены? Будут удалены все фото пользователей, перезапущена отправка заданий, данные из базы и установлена новая дата начала потока введите ее в формате dd.mm.YYYY",
            reply_markup=keyboard_back
        )
        bot.register_next_step_handler(message, get_photo)

    else:
        bot.send_message(
            message.from_user.id,
            message.text,
            reply_markup=keyboard_back
        )


@default_wrapper
def get_user_tasks(message):
    get_tasks_user(message, message.text, admin_panel)


@default_wrapper
def get_table_tasks(message):
    get_tasks_table(message, message.text, admin_panel)


@default_wrapper
def add_balls(message):
    add_to_user(message, message.text, admin_panel)


@default_wrapper
def get_x_table(message):
    get_potok_table(message, message.text, admin_panel)


@default_wrapper
def up_main_tasks(message):
    up_potok_main(message, admin_panel)


@default_wrapper
def up_excel(message):
    up_to_excel(message, admin_panel)


@default_wrapper
def get_potok(message):
    bot.send_message(
        message.from_user.id,
        "Введите сообщение"
    )
    bot.register_next_step_handler(message, send_to_potok, message.text, admin_panel)


@default_wrapper
def get_photo(message):
    reset_config(message, message.text, admin_panel)


def chek_password(message):
    try:
        if message.text == admin_password:
            bot.send_message(
                message.from_user.id,
                "Пароль верен",
                reply_markup=keyboard_admin
            )
            bot.register_next_step_handler(message, admin_panel)
        else:
            bot.send_message(
                message.from_user.id,
                "Неверный пароль"
            )
    except Exception as e:
        logger.exception(e)
