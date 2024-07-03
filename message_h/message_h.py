from telebot import types
from typing import List
from data_base.data_base import Task, Objects
import datetime
from import_for import *



genres: List[str] = [
    'комедия', 'ужасы', 'мелодрама', 'детектив', 'криминал',
    'документальный', 'короткометражка', 'драма', 'мультфильм',
    'фэнтези', 'триллер', 'реальное ТВ', 'музыка', 'игра',
    'концерт', 'семейный', 'боевик', 'спорт', 'приключения',
    'детский', 'мюзикл', 'история', 'военный', 'биография',
    'фантастика', 'для взрослых']



def send_history(message: types.Message) -> None:
    """
    Отправляет историю последних 10 задач пользователю.

    Параметры:
    - message (telebot.types.Message): Объект сообщения от пользователя.

    Возвращает:
    - None

    """
    tasks = Task.select().order_by(Task.due_date.desc()).limit(10)
    for task in tasks:
        if task.genre is not None:
            title = task.title
            due_date = task.due_date.strftime("%d.%m.%Y %H:%M:%S")
            genre = task.genre
            sort_method = task.sort_method
            quantity = task.quantity
            message_text: str = f"Команда: {title}\nВремя: {due_date}\nЖанр: {genre}\nКритерий сортировки: {sort_method}\nКоличество фильмов: {quantity}"
        else:
            message_text: str = f"Команда: {task.title}\nВремя: {task.due_date.strftime('%d.%m.%Y %H:%M:%S')}"

        bot.send_message(message.chat.id, message_text)


def send_welcome(message: types.Message) -> None:
    """
    Отправляет приветственное сообщение и создает задачу для пользователя.

    Параметры:
    - message (telebot.types.Message): Объект сообщения от пользователя.

    Возвращает:
    - None

    """
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


def inline_button(message: types.Message) -> None:
    """
    Отправляет сообщение с кнопками для выбора метода сортировки.

    Параметры:
    - message (telebot.types.Message): Объект сообщения от пользователя.

    Возвращает:
    - None

    """
    markup = types.InlineKeyboardMarkup()
    low_button = types.InlineKeyboardButton(text="По возрастанию ⬆️", callback_data='1')
    high_button = types.InlineKeyboardButton(text="По убыванию ⬇️", callback_data='2')
    markup.add(low_button, high_button)
    bot.send_message(message.chat.id, "Выберите метод сортировки", reply_markup=markup)

