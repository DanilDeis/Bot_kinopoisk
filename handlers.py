from inicialization import *
from telebot import types
from message_handler.message_handler import send_help

load_dotenv(find_dotenv())
api_kinopoisk = os.getenv('api_kinopoisk')
bot = telebot.TeleBot(token=os.getenv('API_TOKEN'))


@bot.message_handler(commands=['start'])
def welcome(message: types.Message) -> None:
    send_welcome(message)
@bot.message_handler(commands=['help'])
def help_comand(message: types.Message) -> None:
    send_help(message)

@bot.message_handler(commands=["history"])
def send(message: types.Message) -> None:
    send_history(message)


@bot.message_handler(commands=['low'])
def inline(message: types.Message) -> None:
    inline_button(message)


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2'])
def han_sort(call: types.CallbackQuery) -> None:
    handle_sorting(call)


@bot.callback_query_handler(func=lambda call: call.data in genres)
def han_ge_selec(call: types.CallbackQuery) -> None:
    handle_genre_selection(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith(tuple(genre + '_' for genre in genres)))
def hane_quant_selec(call: types.CallbackQuery) -> None:
    handle_quantity_selection(call)