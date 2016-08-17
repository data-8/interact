"""Application body"""
from flask import Flask
from . import views


def create_app(config='production'):

    app = Flask(__name__, static_url_path='/static')

    print(' * Running in {} mode'.format(config))
    app.config.from_object('app.config.%sConfig' % config.capitalize())

    return app


