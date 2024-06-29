import telebot

API_TOKEN = '7200709176:AAGdHDdKFQBDH7qtXQqAf3wKlWwK53rotJ8'

bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет я бот для поиска фильмов .
Я здесь чтоб помочь тебе в поиске фильмов на сайте "Kinopoisk"! you!\
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()