import telebot as tb
from flask import Flask, request

from typing import Tuple
from datetime import datetime
from random import choice
from threading import Timer

import config
import words
import json_handler as jh


def init_bot(token: str, url: str) -> Tuple[tb.TeleBot, Flask]:
    
    bot = tb.TeleBot(token, threaded=False)

    bot.remove_webhook()
    bot.set_webhook(url=url)

    app = Flask(__name__)
    
    destinations = jh.Destinations()
    
    def get_reply(command: str, lang: str, rep: dict) -> str:
        reply = rep[command]
        
        try:
            reply = reply[lang]
        except KeyError:
            reply = reply['en']
        
        return reply
    
    @app.route('/' + config.URL.split('/')[-1], methods=['POST'])
    def web_hook():
        update = tb.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return 'ok', 200
    
    def on_timer_sender():
        for dest in destinations.get():
            send_rand_word(dest)
        timer = Timer(60, on_timer_sender)
        timer.start()
    
    def send_rand_word(destination):
        urban = words.RandomUrban()
        message = f"{urban.word}\n\n{urban.meaning}\n\n{urban.example}"
        bot.send_message(destination, message)
    
    @bot.message_handler(commands=['help'])
    def help_answer(message):
        reply = get_reply('help', message.from_user.language_code, replies)
        bot.send_message(message.chat.id, reply)
    
    @bot.message_handler(commands=['start'])
    def start_answer(message):
        added = destinations.add(message.chat.id)
        reply = get_reply(f'start_{added}', message.from_user.language_code, replies)
        bot.send_message(message.chat.id, reply)
        
    @bot.message_handler(commands=['stop'])
    def stop_answer(message):
        removed = destinations.remove(message.chat.id)
        reply = get_reply(f'stop_{removed}', message.from_user.language_code, replies)
        bot.send_message(message.chat.id, reply)
        
    @bot.message_handler(commands=['more'])
    def more_answer(message):
        reply = choice(get_reply('more', message.from_user.language_code, replies))
        bot.send_message(message.chat.id, reply)
        send_rand_word(message.chat.id)
    
    @bot.message_handler(content_types=["text"])
    def default(message):
        reply = get_reply('default', message.from_user.language_code, replies)
        bot.send_message(message.chat.id, reply)

    replies = jh.get_replies()

    utc1 = datetime.utcnow()
    dt = (utc1 - datetime(utc1.year, utc1.month, utc1.day, 18, 0, 0)).total_seconds()
    # t = Timer(abs(60), on_timer_sender)
    # t.start()
    
    return bot, app


my_bot, my_app = init_bot(config.TOKEN, config.URL)
