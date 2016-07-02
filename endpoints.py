from flask import Flask

app = Flask(__name__)

app.config.from_object('settings.DevelopmentConfig')

@app.route('/')
def index():
    return 'Hello World', 200
