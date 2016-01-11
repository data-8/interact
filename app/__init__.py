"""Application body"""
from operator import xor
from app.auth import HubAuth
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from .download_file_and_redirect import download_file_and_redirect
from .pull_from_github import pull_from_github


def create_app(config='production'):

    app = Flask(__name__, static_url_path='/static')

    print(' * Running in {} mode'.format(config))
    app.config.from_object('app.config.%sConfig' % config.capitalize())

    index_args = {
        'file': fields.Str(),

        'git': fields.Str(),
        'path': fields.List(fields.Str()),
    }

    @app.route(app.config['URL'])
    @use_args(index_args)
    def view(args):
        """
        ?file=file_url
        OR (exclusive)
        ?git=github_url&path=file_or_folder_name&path=other_folder

        Authenticates, then downloads file into user's file system.
        """
        is_file_request = ('file' in args)
        is_git_request = ('git' in args and 'path' in args)
        valid_request = xor(is_file_request, is_git_request)
        if not valid_request:
            return "Request was malformed. It must contain either the file " \
                "param or both the git and path params."

        # authenticate() returns either a username as a string or a redirect
        redirection = username = authenticate()
        is_authenticated = isinstance(username, str)
        if not is_authenticated:
            return redirection

        if is_file_request:
            redirection = download_file_and_redirect(
                username=username,
                file_url=args['file'],
                config=app.config,
            )
        elif is_git_request:
            redirection = pull_from_github(
                username=username,
                github_url=args['git'],
                paths=args['path'],
                config=app.config,
            )

        return redirection

    return app


def authenticate():
    """Authenticates the user with the local JupyterHub installation."""
    return HubAuth().authenticate()
