from run import app


@app.route('/')
def index():
    return 'test'
