from callback_handler.callback_h import *
from message_h.message_h import inline_button, send_history, send_welcome
from telebot import types
from import_for import *


@bot.message_handler(commands=['help', 'start'])
def welcome(message: types.Message) -> None:
    send_welcome(message)


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


if __name__ == "__main__":
    bot.polling(none_stop=True)
