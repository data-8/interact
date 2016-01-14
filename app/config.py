import os

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
    # TODO(sam): Remove once things are working
    DEBUG = True

    # URL for users to access
    URL = '/hub/interact/'

    # JupyterHub API token
    API_TOKEN = os.environ['JPY_API_TOKEN']

    # Cookie name?
    COOKIE = 'jupyter-hub-token'

    # where file is copied to
    COPY_PATH = '/home/{username}'

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/user/{username}/notebooks/{destination}'

    # where users are redirect upon git pull success
    GIT_REDIRECT_PATH = '/user/{username}/tree/{destination}'

    # allowed sources for file parameter in query
    ALLOWED_DOMAIN = 'http://data8.org'

    # base_url for the program
    BASE_URL = 'https://ds8.berkeley.edu'

    # alowed file extensions
    ALLOWED_FILETYPES = ['ipynb']

    # app.run parameters
    INIT = {
        'host': '0.0.0.0',
        'port': 8002
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
    COPY_PATH = 'app/static/users/{username}'

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/static/users/{username}/{destination}'

    # where users are redirected upon git pull success
    # This doesn't actually do anything in development since Flask can't serve
    # directories
    GIT_REDIRECT_PATH = None

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

    # where users are redirected upon file download success
    FILE_REDIRECT_PATH = '/static/users/{username}/{destination}'

    # where users are redirected upon git pull success
    GIT_REDIRECT_PATH = None

    # allowed sources for file parameter in query
    ALLOWED_DOMAIN = 'http://localhost:8000'

    # base_url for the program
    BASE_URL = 'http://localhost:8002'

    # allowed file extensions
    ALLOWED_FILETYPES = ['ipynb']
