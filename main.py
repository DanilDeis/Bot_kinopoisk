
import telebot
from telebot import types
from typing import Dict, Any
import requests
import json

API_TOKEN = '7200709176:AAGdHDdKFQBDH7qtXQqAf3wKlWwK53rotJ8'

bot = telebot.TeleBot(API_TOKEN)
genres = [
    'комедия', 'ужасы', 'мелодрама', 'детектив', 'криминал',
    'документальный', 'короткометражка', 'драма', 'мультфильм',
    'фэнтези', 'триллер', 'реальное ТВ', 'музыка', 'игра',
    'концерт', 'семейный', 'боевик', 'спорт', 'приключения',
    'детский', 'мюзикл', 'история', 'военный', 'биография',
    'фантастика', 'для взрослых'
]




@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет я бот для поиска фильмов .
Я здесь чтоб помочь тебе в поиске фильмов на сайте "Kinopoisk"!  Вы можете нажать кнопку /low для поиска фильмов по критериям.\
""")



@bot.message_handler(commands=['low'])
def inline_button(message):
    markup = types.InlineKeyboardMarkup()
    low_button = types.InlineKeyboardButton(text="По возрастанию ⬆️", callback_data='1')
    high_button = types.InlineKeyboardButton(text="По убыванию ⬇️", callback_data='2')
    markup.add(low_button, high_button)
    bot.send_message(message.chat.id, "Выберите метод сортировки", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['1', '2'])
def handle_sorting(call):
    rating = call
    markup = types.InlineKeyboardMarkup()
    genre_buttons = []
    for genre in genres:
        button = types.InlineKeyboardButton(text=genre, callback_data=genre)
        genre_buttons.append(button)
    markup.add(*genre_buttons)
    bot.send_message(call.message.chat.id, "Выберите жанр:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data in genres)
def handle_genre_selection(call):
    quan = call
    markup = types.InlineKeyboardMarkup()
    button_numbers = ["10", "20", "30", "40", "50"]
    buttons = []
    for number in button_numbers:
        callback_data = f"{call.data}_{number}"
        button = types.InlineKeyboardButton(text=number, callback_data=callback_data)
        buttons.append(button)
    markup.add(*buttons)
    bot.send_message(call.message.chat.id, "Выберите количество фильмов:", reply_markup=markup)







bot.polling(none_stop=True)

