"""Application body"""

from flask import Flask
from flask_socketio import SocketIO

import eventlet

socketio = SocketIO(async_mode='eventlet')


def create_app(config='production'):

    app = Flask(__name__, static_url_path='/static')

    print(' * Running in {} mode'.format(config))
    app.config.from_object('app.config.%sConfig' % config.capitalize())

    with app.app_context():
        from . import views

    # setup async sockets
    eventlet.monkey_patch()
    socketio.init_app(app)

    return app


