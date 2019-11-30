from flask_sslify import SSLify
from words_bot import init_bot_app
import config


bot, app = init_bot_app(config.TOKEN, config.URL)
# sslify = SSLify(app)


@app.route('/')
def index():
    return 'test'


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # , port=80)

