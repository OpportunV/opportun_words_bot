from words_bot import init_bot_app
import config


bot, app = init_bot_app(config.TOKEN, config.URL)


if __name__ == '__main__':
    app.run()
