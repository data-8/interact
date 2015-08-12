from flask import Flask


def create_app(config='production'):
	
	app = Flask(__name__)
	
	print(' * Running in %s mode' % config)
	app.config.from_object('app.config.%sConfig' % config.capitalize())
	
	return app