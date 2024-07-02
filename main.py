import telebot
from telebot import types
from peewee import Model, SqliteDatabase, PrimaryKeyField, CharField
import requests
import json

db = SqliteDatabase("my_database.db")
class BaseModel(Model):
    class Meta:
        database = db

class Objects(BaseModel):
    id = PrimaryKeyField(unique=True)
    user_id = CharField()
    rating = CharField(null=True)
    genre = CharField(null=True)
    quan = CharField(null=True)
    class Meta:
        table_name = "objects"

db.create_tables([Objects])

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
    user_id = call.from_user.id
    markup = types.InlineKeyboardMarkup()
    genre_buttons = []
    for genre in genres:
        button = types.InlineKeyboardButton(text=genre, callback_data=genre)
        genre_buttons.append(button)
    markup.add(*genre_buttons)
    bot.send_message(call.message.chat.id, "Выберите жанр:", reply_markup=markup)
    if not Objects.select().where(Objects.user_id == user_id).exists():
        Objects.create(
            user_id=user_id,
            rating=call.data,
            genre=None,
            quan=None
        )

@bot.callback_query_handler(func=lambda call: call.data in genres)
def handle_genre_selection(call):
    user_id = call.from_user.id
    markup = types.InlineKeyboardMarkup()
    button_numbers = ["10", "20", "30", "40", "50"]
    buttons = []
    for number in button_numbers:
        callback_data = f"{call.data}_{number}"
        button = types.InlineKeyboardButton(text=number, callback_data=callback_data)
        buttons.append(button)
    markup.add(*buttons)
    bot.send_message(call.message.chat.id, "Выберите количество фильмов:", reply_markup=markup)
    if Objects.select().where(Objects.user_id == user_id).exists():
        obj = Objects.get(Objects.user_id == user_id)
        obj.genre = call.data
        obj.save()
    else:
        Objects.create(
            user_id=user_id,
            genre=call.data,
            quan=None
        )
@bot.callback_query_handler(func=lambda call: call.data.startswith(tuple(genre + '_' for genre in genres)))
def handle_quantity_selection(call):
    user_id = call.from_user.id
    selected_option = call.data.split('_')[-1]
    bot.send_message(call.message.chat.id, f"Вы выбрали {selected_option} фильмов.")
    if Objects.select().where(Objects.user_id == user_id).exists():
        obj = Objects.get(Objects.user_id == user_id)
        obj.quan = selected_option
        obj.save()
    all_objects = Objects.select().where(Objects.user_id == user_id)
    results = send_req(all_objects)
    str_viev(results, call.message.chat.id)


def send_req(all_objects):
    for obj in all_objects:
        rating = obj.rating
        quan = obj.quan
        genre = obj.genre

    api_kinopoisk = "8SFS5TR-FZD45JS-PKZP84J-GZGW8W9"
    url = 'https://api.kinopoisk.dev/v1.4/movie'
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_kinopoisk,
    }

    if rating == '1':
        sort_type = '1'
    else:
        sort_type = '-1'

    params = {
        "limit": quan,
        'genres.name': genre,
        "sortField": "rating.kp",
        "sortType": sort_type,
        "selectFields": ['id', 'name', 'type', 'year', 'rating', 'genres']
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return 'Не удалось выполнить поиск'
    else:
        return json.loads(response.text)


def str_viev(result, chat_id):
    total_str = ""
    count = 0
    for key, value in result.items():
        if isinstance(value, list):
            for elem in value:
                if isinstance(elem, dict):
                    count += 1
                    all_str = f"{str(count)}) {elem['name']} - {elem['year']} - kp rating {elem['rating']['kp']} - imdb rating {elem['rating']['imdb']}\n"
                    total_str += all_str

    bot.send_message(chat_id, total_str)




bot.polling(none_stop=True)

