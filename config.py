import telebot
from datetime import date, time

token = '2134782586:AAFPXNhYXej4giO8LQfHjAztQ7S0o2cKhUQ'
start_date = date(2021, 11, 18)

main_hours = 3

bot = telebot.TeleBot(token)

scores = {
    "Шичко": 5,
    "Планирование": 5,
    "Благодарности": 5,
    "Книга": 50,
    "Аудио-книга": 30,
    "Прямой эфир": 10,
    "Чистый день 1":5,
    "Чистый день 2":10,
    "Тренировка": 10,
    "Пробежка":10,
    "Прогулка":5
}


regular_tasks = {
    'shichko': 0,
    'planning': 0,
    'thanks': 0,
    'main_task': 0,
    'book': 0,
    'audio_book': 0,
    'analyzes': 0,
    'sport': 0,
    'jogging': 0,
    'fitness-game': 0,
    'walk': 0,
    'clean_day': 0,
    'stream': 0
}
