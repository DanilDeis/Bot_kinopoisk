from handlers import welcome, help_comand, send, inline, han_sort, han_ge_selec, hane_quant_selec
import argparse
from config import bot

def main():
    parser = argparse.ArgumentParser(description='Вы можете нажать кнопку /low для поиска фильмов по критериям(нажимайте на кнопки до появления результатов вашего поиска).Команда /history - выводит 10 последних команд бота.')
    args = parser.parse_args()

if __name__ == "__main__":
    main()
    bot.polling(none_stop=True)
