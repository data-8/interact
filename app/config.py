

class Config:
	"""General configurations"""
	DEBUG = False
	TESTING = False
	
	# passed to app.run as kwargs
	INIT = {
		'host': '127.0.0.1',
	    'port': 8002
	}


class ProductionConfig(Config):
	"""Configuration for production"""
	pass


class DevelopmentConfig(Config):
	"""Configuration for development mode"""
	DEBUG = True


class TestConfig(Config):
	"""Configuration for testing mode"""
	TESTING = True