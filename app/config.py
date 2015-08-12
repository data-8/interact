

class Config:
	"""General configurations"""
	DEBUG = False
	TESTING = False

	URL = '/'  # URL for users to access
	COPY_PATH = 'users/{username}'  # where file is copied to
	REDIRECT_PATH = ''  # where users are redirected upon success
	
	BASE_URL = 'http://localhost:8002'
	
	ALLOWED_DOMAIN = BASE_URL
	ALLOWED_FILETYPES = ['ipynb']
	
	# passed to app.run as kwargs
	INIT = {
		'host': '127.0.0.1',
	    'port': 8002
	}


class ProductionConfig(Config):
	"""Configuration for production"""
	URL = '/hub/interact'
	COPY_PATH = '/home/{username}'
	
	ALLOWED_DOMAIN = 'http://data8.org'
	
	BASE_URL = 'http://dsten.berkeley.edu'


class DevelopmentConfig(Config):
	"""Configuration for development mode"""
	DEBUG = True


class TestConfig(Config):
	"""Configuration for testing mode"""
	TESTING = True