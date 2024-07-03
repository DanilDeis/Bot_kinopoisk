import datetime
import telebot
from telebot import types
import requests
import json
from peewee import (
    AutoField,
    CharField,
    DateField,
    ForeignKeyField,
    Model,
    SqliteDatabase, PrimaryKeyField, DateTimeField
)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
bot = telebot.TeleBot(token=os.getenv('API_TOKEN'))
api_kinopoisk = os.getenv('api_kinopoisk')
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
    sort_method = CharField(null=True)

    class Meta:
        table_name = "objects"


class Task(BaseModel):
    task_id = AutoField()
    user = ForeignKeyField(Objects, backref="tasks")
    title = CharField()
    due_date = DateTimeField()
    genre = CharField(null=True)
    sort_method = CharField(null=True)
    quantity = CharField(null=True)
    class Meta:
        table_name = "tasks"



db.create_tables([Objects,Task])



genres = [
    'комедия', 'ужасы', 'мелодрама', 'детектив', 'криминал',
    'документальный', 'короткометражка', 'драма', 'мультфильм',
    'фэнтези', 'триллер', 'реальное ТВ', 'музыка', 'игра',
    'концерт', 'семейный', 'боевик', 'спорт', 'приключения',
    'детский', 'мюзикл', 'история', 'военный', 'биография',
    'фантастика', 'для взрослых'
]

@bot.message_handler(commands=["history"])
def send_histori(message):
    tasks = Task.select().order_by(Task.due_date.desc()).limit(10)
    for task in tasks:
        if task.genre is not None:
            title = task.title
            due_date = task.due_date.strftime("%d.%m.%Y %H:%M:%S")
            genre = task.genre
            sort_method = task.sort_method
            quantity = task.quantity
            message_text = f"Команда: {title}\nВремя: {due_date}\nЖанр: {genre}\nКритерий сортировки: {sort_method}\nКоличество фильмов: {quantity}"
        else:
            message_text = f"Команда: {task.title}\nВремя: {task.due_date.strftime('%d.%m.%Y %H:%M:%S')}"

        bot.send_message(message.chat.id, message_text)
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет я бот для поиска фильмов .
Я здесь чтоб помочь тебе в поиске фильмов на сайте "Kinopoisk"!  Вы можете нажать кнопку /low для поиска фильмов по критериям.\
""")
    user_id = message.from_user.id
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    Task.create(
        user=Objects.get_or_create(user_id=user_id)[0],
        title=message.text,
        due_date=formatted_datetime,
        genre=None,
        sort_method=None,
        quantity=None
    )



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
    sort_method = call.data.split('_')[-1]
    markup = types.InlineKeyboardMarkup()
    genre_buttons = []
    for genre in genres:
        button = types.InlineKeyboardButton(text=genre, callback_data=genre)
        genre_buttons.append(button)
    markup.add(*genre_buttons)
    bot.send_message(call.message.chat.id, "Выберите жанр:", reply_markup=markup)
    if Objects.select().where(Objects.user_id == user_id).exists():
        obj = Objects.get(Objects.user_id == user_id)
        obj.sort_method = sort_method
        obj.save()
    else:
        Objects.create(
            user_id=user_id,
            rating=None,
            genre=None,
            quan=None,
            sort_method=sort_method
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
        Task.create(
            user=obj,
            title="/low",
            due_date=datetime.datetime.now(),
            genre=obj.genre,
            sort_method=obj.sort_method,
            quantity=selected_option
        )
        all_objects = Objects.select().where(Objects.user_id == user_id)
        results = send_req(all_objects, api_kinopoisk)
        str_view(results, call.message.chat.id)
    else:
        bot.send_message(call.message.chat.id, "Ошибка: не найден пользователь с таким ID.")


def send_req(all_objects, api_kinopoisk ):
    for obj in all_objects:
        rating = obj.rating
        quan = obj.quan
        genre = obj.genre
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


def str_view(result, chat_id):
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