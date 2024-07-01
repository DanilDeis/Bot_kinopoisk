
import telebot
from telebot import types

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

API_TOKEN = '7200709176:AAGdHDdKFQBDH7qtXQqAf3wKlWwK53rotJ8'

bot = telebot.TeleBot(API_TOKEN)



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
    sorting_method = call.data
    markup = types.InlineKeyboardMarkup()
    genre_buttons = [
        types.InlineKeyboardButton(text="комедия", callback_data="комедия"),
        types.InlineKeyboardButton(text="ужасы", callback_data="ужасы"),
        types.InlineKeyboardButton(text="мелодрама", callback_data="мелодрама"),
        types.InlineKeyboardButton(text="детектив", callback_data="детектив"),
        types.InlineKeyboardButton(text="криминал", callback_data="криминал"),
        types.InlineKeyboardButton(text="документальный", callback_data="документальный"),
        types.InlineKeyboardButton(text="короткометражка", callback_data="короткометражка"),
        types.InlineKeyboardButton(text="драма", callback_data="драма"),
        types.InlineKeyboardButton(text="мультфильм", callback_data="мультфильм"),
        types.InlineKeyboardButton(text="фэнтези", callback_data="фэнтези"),
        types.InlineKeyboardButton(text="триллер", callback_data="триллер"),
        types.InlineKeyboardButton(text="реальное ТВ", callback_data="реальное ТВ"),
        types.InlineKeyboardButton(text="музыка", callback_data="музыка"),
        types.InlineKeyboardButton(text="игра", callback_data="игра"),
        types.InlineKeyboardButton(text="концерт", callback_data="концерт"),
        types.InlineKeyboardButton(text="семейный", callback_data="семейный"),
        types.InlineKeyboardButton(text="боевик", callback_data="боевик"),
        types.InlineKeyboardButton(text="спорт", callback_data="спорт"),
        types.InlineKeyboardButton(text="приключения", callback_data="приключения"),
        types.InlineKeyboardButton(text="детский", callback_data="детский"),
        types.InlineKeyboardButton(text="мюзикл", callback_data="мюзикл"),
        types.InlineKeyboardButton(text="история", callback_data="история"),
        types.InlineKeyboardButton(text="военный", callback_data="военный"),
        types.InlineKeyboardButton(text="биография", callback_data="биография"),
        types.InlineKeyboardButton(text="фантастика", callback_data="фантастика"),
        types.InlineKeyboardButton(text="для взрослых", callback_data="для взрослых"),
    ]
    markup.add(*genre_buttons)
    bot.send_message(call.message.chat.id, "Выберите жанр:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in [
    'комедия', 'ужасы', 'мелодрама', 'детектив', 'криминал',
    'документальный', 'короткометражка', 'драма', 'мультфильм',
    'фэнтези', 'триллер', 'реальное ТВ', 'музыка', 'игра',
    'концерт', 'семейный', 'боевик', 'спорт', 'приключения',
    'детский', 'мюзикл', 'история', 'военный', 'биография',
    'фантастика', 'для взрослых'
])
def handle_genre_selection(call):
    markup = types.InlineKeyboardMarkup()
    list_10 = types.InlineKeyboardButton(text="10 фильмов", callback_data="10")
    list_20 = types.InlineKeyboardButton(text="20 фильмов", callback_data="20")
    list_30 = types.InlineKeyboardButton(text="30 фильмов", callback_data="30")
    list_40 = types.InlineKeyboardButton(text="40 фильмов", callback_data="40")
    list_50 = types.InlineKeyboardButton(text="50 фильмов", callback_data="50")
    markup.row(list_10, list_20)
    markup.row(list_30, list_40, list_50)
    bot.send_message(call.message.chat.id, "Выберите количество фильмов:", reply_markup=markup)


bot.polling(none_stop=True)