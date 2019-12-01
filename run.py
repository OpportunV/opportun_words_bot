from words_bot import init_bot
from flask_app import init_app
import config


app = init_app()
bot = init_bot(config.TOKEN, config.URL, app)


if __name__ == '__main__':
    app.run()
