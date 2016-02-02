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

        'repo': fields.Str(),
        'path': fields.List(fields.Str()),
    }

    @app.route(app.config['URL'])
    @use_args(index_args)
    def view(args):
        """
        ?file=public_file_url
        Example: ?file=http://localhost:8000/README.md

        OR (exclusive)

        ?repo=data8_github_repo_name&path=file_or_folder_name&path=other_folder
        Example: ?repo=textbook&path=notebooks&path=chapter1%2Fintroduction.md

        Authenticates, then downloads file / git pulls into user's file system.
        Note: Only the gh-pages branch is pulled from Github.
        """
        is_file_request = ('file' in args)
        is_git_request = ('repo' in args and 'path' in args)
        valid_request = xor(is_file_request, is_git_request)
        if not valid_request:
            return "Request was malformed. It must contain either the file " \
                "param or both the repo and path params."

        hubauth = HubAuth()

        # authenticate() returns either a username as a string or a redirect
        redirection = username = hubauth.authenticate()
        is_authenticated = isinstance(username, str)
        if not is_authenticated:
            return redirection

        # Start the user's server if necessary
        if not hubauth.notebook_server_exists(username):
            return '/hub/home'

        if is_file_request:
            redirection = download_file_and_redirect(
                username=username,
                file_url=args['file'],
                config=app.config,
            )
        elif is_git_request:
            redirection = pull_from_github(
                username=username,
                repo_name=args['repo'],
                paths=args['path'],
                config=app.config,
            )

        return redirection

    return app


