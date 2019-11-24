from typing import Tuple
from config import TOKEN
import telebot as tb
import googletrans as gt


def init_bot(token) -> tb.TeleBot:
    bot = tb.TeleBot(token)
    
    @bot.message_handler(commands=['help'])
    def help_answer(message):
        print(message)
        bot.send_message(message.chat.id, "We all are helpless...")

    @bot.message_handler(content_types=["text"])
    def echo(message):
        bot.send_message(message.chat.id, "I don't want to live!!!\nHlep me!")
    
    return bot


def translate(phrase: str, source='en', target='ru') -> str:
    return ''


def get_rand_urban_word() -> Tuple[str, str]:
    return '', ''


def add_to_to_learn(word, meaning) -> None:
    pass
    

def del_from_to_learn(word, meaning) -> None:
    pass

   
def main():
    bot = init_bot(TOKEN)
    bot.polling(none_stop=True)
    

if __name__ == '__main__':
    main()
