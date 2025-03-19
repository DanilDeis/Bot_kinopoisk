import datetime
from telebot import types
from api_kino.api_kinopoisk import send_req, str_view
from data_base.data_base import Task, Objects
from message_handler.message_handler import genres
from config import bot, api_kinopoisk

def handle_sorting(call: types.CallbackQuery) -> None:
    """
    Обрабатывает выбор пользователя по методу сортировки.

    Параметры:
    - call (telebot.types.CallbackQuery): Объект callback-запроса от пользователя.

    Возвращает:
    - None

    """

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


def handle_genre_selection(call: types.CallbackQuery) -> None:
    """
    Обрабатывает выбор пользователя по жанру.

    Параметры:
    - call (telebot.types.CallbackQuery): Объект callback-запроса от пользователя.

    Возвращает:
    - None

    """
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


def handle_quantity_selection(call: types.CallbackQuery) -> None:
    """
    Обрабатывает выбор пользователя по количеству фильмов.

    Параметры:
    - call (telebot.types.CallbackQuery): Объект callback-запроса от пользователя.

    Возвращает:
    - None

    """

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