from telebot import *


keyboard_mind = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Шичко')
button2 = types.KeyboardButton('Благодарности')
button3 = types.KeyboardButton('Планирование')
button4 = types.KeyboardButton('Основные')
keyboard_mind.row(button1, button2, button3, button4)
button5 = types.KeyboardButton('Книга')
button6 = types.KeyboardButton('Аудио-книга')
button7 = types.KeyboardButton('Посещение прямых эфиров')
button8 = types.KeyboardButton('Видеолекции')
keyboard_mind.row(button5, button6, button7, button8)
button9 = types.KeyboardButton('Назад')
button10 = types.KeyboardButton('Эфиры')
keyboard_mind.row(button9, button10)


keyboard_health = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Зарегистрировать чистый день')
button2 = types.KeyboardButton('Фитнес игра')
button3 = types.KeyboardButton('Контрастный душ')
keyboard_health.row(button1, button2, button3)
button4 = types.KeyboardButton('Назад')
keyboard_health.row(button4)

keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Мышление')
button2 = types.KeyboardButton('Здоровье')
button3 = types.KeyboardButton('Статистика')
keyboard_main.add(button1, button2, button3)

keyboard_stats_b = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Текущая неделя среди новичков')
button2 = types.KeyboardButton('За все время среди новичков')
button3 = types.KeyboardButton('Среди всех этапов')
button4 = types.KeyboardButton('Моя статистика')
keyboard_stats_b.row(button1, button2, button3)
keyboard_stats_b.row(button4)
button5 = types.KeyboardButton('Назад')
keyboard_stats_b.row(button5)

keyboard_other = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('За все среди текущего этапа')
button2 = types.KeyboardButton('Среди всех этапов')
button3 = types.KeyboardButton('Моя статистика')
keyboard_other.row(button1, button2)
keyboard_other.row(button3)
button4 = types.KeyboardButton('Назад')
keyboard_other.row(button4)

keyboard_programs = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Новичок', callback_data='beginer')
button2 = types.InlineKeyboardButton('Старт', callback_data='starter')
button3 = types.InlineKeyboardButton('Лидер', callback_data='leader')
button4 = types.InlineKeyboardButton('Эксперт', callback_data='profi')
keyboard_programs.row(button1, button2, button3, button4)

keyboard_switch = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Назад')
button2 = types.KeyboardButton('Подтвердить')
keyboard_switch.add(button1, button2)

keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('Просмотр выполненных заданий пользователя ["X"]')
button2 = types.KeyboardButton('Просмотр таблицы заданий типа ["Y"]')
button3 = types.KeyboardButton('Добавить или отнять ["Y"] баллов у пользователя ["X"]')
button4 = types.KeyboardButton('Выгрузить таблицу текущей недели(у новичков)')
button5 = types.KeyboardButton('Выгрузить таблицу потока ["X"]')
button6 = types.KeyboardButton('Выгрузить общую таблицу среди всех потоков')
button7 = types.KeyboardButton('Загрузить ежедневные задания для потока ["X"]')
button8 = types.KeyboardButton('Загрузить новую таблицу пользователей')
button9 = types.KeyboardButton('Отправить сообщение для потока ["X"]')
keyboard_admin.row(button1, button2, button3)
keyboard_admin.row(button4, button5, button6)
keyboard_admin.row(button7, button8, button9)
button10 = types.KeyboardButton('Назад')
button11 = types.KeyboardButton('Скачать фото')
keyboard_admin.row(button10, button11)

keyboard_fit_game = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton('1 уровень')
button2 = types.KeyboardButton('2 уровень')
button3 = types.KeyboardButton('3 уровень')
button4 = types.KeyboardButton('4 уровень')
button5 = types.KeyboardButton('5 уровень')
button6 = types.KeyboardButton('6 уровень')
button7 = types.KeyboardButton('7 уровень')
button8 = types.KeyboardButton('8 уровень')
button9 = types.KeyboardButton('9 уровень')
button10 = types.KeyboardButton('10 уровень')
button11 = types.KeyboardButton('Назад')
keyboard_fit_game.row(button1, button2)
keyboard_fit_game.row(button3, button4)
keyboard_fit_game.row(button5, button6)
keyboard_fit_game.row(button7, button8)
keyboard_fit_game.row(button9, button10)
keyboard_fit_game.row(button11)
