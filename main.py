from handlers import *
import argparse
from config import *


def main():
    parser = argparse.ArgumentParser(description='Вы можете нажать кнопку /low для поиска фильмов по критериям(нажимайте на кнопки до появления результатов вашего поиска).Команда /history - выводит 10 последних команд бота.')
    args = parser.parse_args()


if __name__ == "__main__":
    main()
    bot.polling(none_stop=True)
