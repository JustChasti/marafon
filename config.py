import telebot
from datetime import date

token = '2134782586:AAFPXNhYXej4giO8LQfHjAztQ7S0o2cKhUQ'
start_date = date(2021, 11, 18)

bot = telebot.TeleBot(token)

scores = {
    "Шичко": 10,
    "Планирование": 10,
    "Благодарности": 10
}
