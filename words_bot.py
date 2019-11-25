from typing import Tuple
import config
import telebot as tb
import googletrans as gt
from flask import Flask, request


def init_bot(token: str, url: str) -> Tuple[tb.TeleBot, Flask]:
    bot = tb.TeleBot(token, threaded=False)
    
    bot.remove_webhook()
    bot.set_webhook(url=url)
    
    app = Flask(__name__)
    
    @app.route('/' + config.URL.split('/')[-1], methods=['POST'])
    def web_hook() -> Tuple[str, int]:
        update = tb.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'ok', 200
    
    @bot.message_handler(commands=['help'])
    def help_answer(message):
        print(message)
        bot.send_message(message.chat.id, "We all are helpless...")

    @bot.message_handler(content_types=["text"])
    def echo(message):
        bot.send_message(message.chat.id, "I don't want to live!!!\nHlep me!")
    
    return bot, app


def translate(phrase: str, source='en', target='ru') -> str:
    return ''


def get_rand_urban_word() -> Tuple[str, str]:
    return '', ''


def add_to_to_learn(word, meaning) -> None:
    pass
    

def del_from_to_learn(word, meaning) -> None:
    pass


my_bot, my_app = init_bot(config.TOKEN, config.URL)
