import os
import shutil
from datetime import date,  datetime
from config import bot
from config import start_date
from modules.keyboards import keyboard_admin
from loguru import logger


def reset_config(message, data, admin_panel):
    try:
        shutil.rmtree('user-data')
        os.mkdir('user-data')
        start_date = datetime.strptime(data, '%d.%m.%Y').date()
        bot.send_message(
                message.from_user.id,
                "Данные сброшены",
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
