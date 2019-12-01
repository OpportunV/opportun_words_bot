from words_bot import init_bot
from flask_app import app
import view
import config


bot = init_bot(config.TOKEN, config.URL, app)


if __name__ == '__main__':
    app.run()
