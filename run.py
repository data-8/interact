"""Initializer for app"""
import tornado.ioloop

from app.interact_app import InteractApp
from app.config import config_for_env
from app.util import logger

import argparse

parser = argparse.ArgumentParser(
    description='Controls deployment configuration')
parser.add_argument('--production', action='store_true',
                    default=True, help='Launch in production mode')
parser.add_argument('--development', action='store_true',
                    default=False, help='Launch in developer mode')
parser.add_argument('--test', action='store_true',
                    default=False, help='*Used only by automated tests*')

args = parser.parse_args()
env_name = 'production'

for conf in ['production', 'development', 'test']:
    arg = getattr(args, conf)
    env_name = conf if arg else env_name

config = config_for_env(env_name)


if __name__ == '__main__':
    app = InteractApp(config=config)
    app.listen(config['PORT'])

    logger.info('Starting interact app on port {}'.format(config['PORT']))
    tornado.ioloop.IOLoop.current().start()
