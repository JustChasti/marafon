import telebot
from datetime import date


# настройки самого бота
token = '2134782586:AAFPXNhYXej4giO8LQfHjAztQ7S0o2cKhUQ'
admin_password = 'admin01'

# очки меняются
scores = {
    "Шичко": 5,
    "Планирование": 5,
    "Благодарности": 5,
    "Книга": 50,
    "Аудио-книга": 30,
    "Прямой эфир": 10,
    "Чистый день 1": 5,
    "Чистый день 2": 10,
    "Тренировка": 10,
    "Пробежка": 10,
    "Прогулка": 5
}

# лист заданий
regular_tasks = {
    'shichko': 0,
    'planning': 0,
    'thanks': 0,
    'main_tasks': 0,
    'book': 0,
    'audio_book': 0,
    'sport': 0,
    'fitness-game': 0,
    'walk': 0,
    'clean_day': 0,
    'stream': 0
}

# дата начала нового потока (потом добавить в админ панель функцию изменения этой штуки)
start_date = date(2021, 12, 10)

# это часы отправки утренних напоминаний для reminder 
main_hours = 19

# собсна бот
bot = telebot.TeleBot(token)

# ссылка для git clone
link = 'https://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:x-oauth-basic@github.com/JustChasti/marafon.git'
link = 'docker attach sayno_bot'

"""
    Настройки для базы
    для винды
        base_domen = "localhost"
        base_port = 27017

    для докера
        base_domen = "mongo"
        base_port = 27017
        client_name = 'saynotes'

    имя клиента и имя коллекции настроить под себя
"""
base_domen = "localhost"
base_port = 27017
client_name = 'saynotes'