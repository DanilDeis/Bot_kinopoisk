from typing import Dict, Any
import requests
import json

def send_req(rating: str, genre: str, quan: str) -> [str, Dict[str, Any]]:
    api_kinopoisk= "8SFS5TR-FZD45JS-PKZP84J-GZGW8W9"
    url = 'https://api.kinopoisk.dev/v1.4/movie'
    headers = {

        "accept": "application/json",

        "X-API-KEY": api_kinopoisk,
    }
    if rating == '1':
        sort_type = '1'
    else:
        sort_type = '-1'
    params = {"limit": quan,

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


def str_viev(result):
    total_str = " "
    count = 0
    for key, value in result.items():
        if isinstance(value, list):
            for elem in value:
                if isinstance(elem, dict):
                    count += 1
                    all_str = f"{str(count)}) {elem['name']} - {elem['year']} - kp rating {elem['rating']['kp']} - imdb rating {elem['rating']['imdb']}\n"
                    total_str += all_str
    return total_str




