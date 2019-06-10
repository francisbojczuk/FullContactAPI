from flask import Flask
from flask import render_template

from config import app_config

def create_app(config_name):
    app =  Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    @app.route('/')
    @app.route('/index')
    def index():
        user = {'username': 'Miguel'}
        return render_template('index.html', title='Home', user=user)

    return app