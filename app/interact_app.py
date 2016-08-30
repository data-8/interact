import os
import tornado.web
from tornado.options import define

from .handlers import LandingHandler, RequestHandler


class InteractApp(tornado.web.Application):
    """
    Entry point for the interact app.
    """
    def __init__(self, config=None):
        # Terrible hack to get config object in global namespace. This allows
        # us to use options.config to get the global config object.
        #
        # TODO(sam): Replace with a better solution
        define('config', config)

        base_url = config['URL']
        socket_url = config['URL'] + 'socket/(\w+)'

        settings = dict(
            debug=True,
            serve_traceback=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path="/srv/interact/app/static",
            static_url_prefix="/hub/interact/static/",
        )

        static_url = "r{}/static/(.*)".format(base_url)
        handlers = [
            (base_url, LandingHandler),
            (socket_url, RequestHandler),
        ]

        super(InteractApp, self).__init__(handlers, **settings)
