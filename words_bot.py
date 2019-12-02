from typing import Union, List, Optional
from datetime import datetime
from random import choice
from threading import Timer

import telebot as tb
from flask import Flask, request

import config
import words
import json_handler as jh


def init_bot(token: str, url: Optional[str] = None, app: Optional[Flask] = None) -> tb.TeleBot:
    """if app is None there is no need to pass url, but if app is not None url is required"""
    
    bot = tb.TeleBot(token, threaded=False)
    
    if app is not None:
        bot.remove_webhook()
        bot.set_webhook(url=url)
        
        @app.route('/' + url.split('/')[-1], methods=['POST'])
        def web_hook():
            update = tb.types.Update.de_json(request.stream.read().decode('utf-8'))
            bot.process_new_updates([update])
            return 'ok', 200
    
    destinations = jh.Destinations()
    
    def get_reply(command: str, lang: str, rep: dict) -> str:
        reply = rep[command]
        
        try:
            reply = reply[lang]
        except KeyError:
            reply = reply['en']
        
        return reply
    
    def on_timer_sender():
        send_rand_word(destinations.get())
        timer = Timer(config.send_delta_time, on_timer_sender)
        timer.start()
    
    def send_rand_word(destination: Union[int, List[int]]):
        urban = words.RandomUrban()
        message = f"{urban.word}\n\n{urban.meaning}\n\n{urban.example}\n{urban.link}"
        try:
            for dest in destination:
                bot.send_message(dest, message, disable_web_page_preview=True)
        except TypeError:
            bot.send_message(destination, message, disable_web_page_preview=True)
    
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
    dt = (datetime(utc1.year, utc1.month, utc1.day, 18, 25, 0) - utc1).total_seconds()
    dt = (dt + config.send_delta_time) % config.send_delta_time
    t = Timer(dt, on_timer_sender)
    t.start()
    
    return bot


if __name__ == '__main__':
    tbot = init_bot(config.TOKEN)
    tbot.remove_webhook()
    tbot.polling(none_stop=True)
