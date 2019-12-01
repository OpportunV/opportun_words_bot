from flask import Flask


def init_app() -> Flask:
    app = Flask(__name__)
    
    return app
