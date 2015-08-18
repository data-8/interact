

class Config:
	"""General configurations"""
	
	# testing parameters
	DEBUG = False
	TESTING = False
	
	# passed to app.run as kwargs
	INIT = {
		'host': '127.0.0.1',
	    'port': 8002
	}


class ProductionConfig(Config):
	"""Configuration for production"""
	
	# URL for users to access
	URL = '/hub/interact'
	
	# JupyterHub API token
	API_TOKEN = 'your_token_here'

	# Cookie name?
	COOKIE = 'interact'

	# where file is copied to
	COPY_PATH = '/home/{username}'
	
	# where users are redirected upon success
	REDIRECT_PATH = '/user/{username}/notebooks/{path}'
	
	# allowed sources for file parameter in query
	ALLOWED_DOMAIN = 'http://data8.org'
	
	# base_url for the program
	BASE_URL = 'http://dsten.berkeley.edu'

	# alowed file extensions
	ALLOWED_FILETYPES = ['ipynb']
	
	# app.run parameters
	INIT = {
		'host': '127.0.0.1',
	    'port': 80
	}


class DevelopmentConfig(Config):
	"""Configuration for development mode"""
	
	# testing parameters
	DEBUG = True

	# URL for users to access
	URL = '/'

	# JupyterHub API token
	API_TOKEN = 'your_token_here'

	# Cookie name?
	COOKIE = 'interact'

	# where file is copied to
	COPY_PATH = 'app/static/users/{username}/{destination}'

	# where users are redirected upon success
	REDIRECT_PATH = '/static/users/{username}/{destination}'

	# allowed sources for file parameter in query
	ALLOWED_DOMAIN = 'http://localhost:8000'

	# base_url for the program
	BASE_URL = 'http://localhost:8002'

	# allowed file extensions
	ALLOWED_FILETYPES = ['ipynb']


class TestConfig(Config):
	"""Configuration for testing mode"""
	
	# testing parameters
	TESTING = True

	# URL for users to access
	URL = '/'

	# JupyterHub API token
	API_TOKEN = 'your_token_here'

	# Cookie name?
	COOKIE = 'interact'

	# where file is copied to
	COPY_PATH = 'app/static/users/{username}'

	# where users are redirected upon success
	REDIRECT_PATH = '/static/users/{username}/{destination}'

	# allowed sources for file parameter in query
	ALLOWED_DOMAIN = 'http://localhost:8000'

	# base_url for the program
	BASE_URL = 'http://localhost:8002'

	# allowed file extensions
	ALLOWED_FILETYPES = ['ipynb']