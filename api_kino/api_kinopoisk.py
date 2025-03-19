from typing import List, Union
import requests
import json
from data_base.data_base import Objects
from config import bot

def send_req(all_objects: List[Objects], api_kinopoisk: str) -> Union[str, dict]:
    """
    Отправляет запрос к API Kinopoisk для получения фильмов.

    Параметры:
    - all_objects (List[Objects]): Список объектов пользователей для поиска фильмов.
    - api_kinopoisk (str): Ключ API для Kinopoisk.

    Возвращает:
    - Union[str, dict]: Возвращает либо текст ошибки, либо словарь с результатами поиска.

    """
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


def str_view(result: dict, chat_id: str) -> None:
    """
    Формирует и отправляет сообщение с результатами поиска фильмов.

    Параметры:
    - result (dict): Словарь с результатами поиска фильмов.
    - chat_id (str): ID чата, куда отправлять сообщение.

    Возвращает:
    - None

    """
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