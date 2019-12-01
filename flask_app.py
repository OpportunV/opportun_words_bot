from flask import Flask


def init_app() -> Flask:
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return 'test'
    
    return app
