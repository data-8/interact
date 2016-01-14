"""Initializer for app"""
from app import create_app

import argparse

parser = argparse.ArgumentParser(description='Controls deployment configuration')
parser.add_argument('--production', action='store_true',
                    default=False, help='Launch in production mode')
parser.add_argument('--development', action='store_true',
                    default=False, help='Launch in developer mode')
parser.add_argument('--test', action='store_true',
                    default=False, help='*Used only by automated tests*')

args, config = parser.parse_args(), 'production'

for conf in ['production', 'development', 'test']:
    arg = getattr(args, conf)
    config = conf if arg else config

app = create_app(config=config)

if __name__ == '__main__':
    app.run(**app.config['INIT'])
