from loguru import logger
from telebot import *
from config import bot


def try_wrapper(function):
    def wrapper(message):
        try:
            function(message)
        except Exception as e:
            logger.exception(e)
            bot.send_message(message.from_user.id, 'ошибка')
            bot.send_message(362340468, str(e))
    return wrapper
