import types
from dotenv import load_dotenv, find_dotenv
import os
import telebot
from callback_handler.callback_h import handle_sorting, handle_genre_selection, handle_quantity_selection
from message_handler.message_handler import send_welcome, send_history, inline_button, genres


load_dotenv(find_dotenv())
api_kinopoisk = os.getenv('api_kinopoisk')
bot = telebot.TeleBot(token=os.getenv('API_TOKEN'))