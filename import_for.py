from dotenv import load_dotenv, find_dotenv
import os
import telebot


load_dotenv(find_dotenv())
api_kinopoisk = os.getenv('api_kinopoisk')
bot = telebot.TeleBot(token=os.getenv('API_TOKEN'))