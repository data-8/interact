"""Views for Interact application, which currently includes

- Landing : with three options for unauthenticated users (1) download zip or
            (2) authenticate and commence copying
- Progress : page containing live updates on server's progress, redirects to
             new content once pull or clone is complete
"""

from app.auth import HubAuth
from flask import current_app
from flask import redirect
from flask import render_template
from flask import url_for
from operator import xor
from threading import Thread
from webargs import fields
from webargs.flaskparser import use_args

from . import util
from .download_file_and_redirect import download_file_and_redirect
from .pull_from_github import pull_from_github

index_args = {
    'file': fields.Str(),

    'repo': fields.Str(),
    'path': fields.List(fields.Str()),
}


@current_app.route(current_app.config['URL'])
@use_args(index_args)
def landing(args):
    """Landing page containing option to download OR (exclusive) authenticate.

    Option 1
    --------

        ?file=public_file_url

    Example: ?file=http://localhost:8000/README.md

    Authenticates, then downloads file into user's system.

    Option 2
    --------

        ?repo=data8_github_repo_name&path=file_or_folder_name&path=other_folder

    Example: ?repo=textbook&path=notebooks&path=chapter1%2Fintroduction.md

    Authenticates, then pulls content into user's file system.
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
        return render_template(
            'landing.html',
            authenticate_link=redirection.location,
            download_links=util.generate_git_download_link(args))

    thread = Thread(
        target=execute_request,
        args=(current_app.app_context(),
              hubauth,
              username,
              is_file_request,
              args))
    thread.start()
    return redirect(url_for('progress', username=username))


def execute_request(context, hubauth, username, is_file_request, args):
    """Execute the request -- either a file load or a git pull.

    This process is ideally run on a separate thread, as all methods in here
    emit broadcasts to user-specific namespaces. In this case, the namespaces
    are uniquely identified by the user's `username`.
    """
    with context:

        # Start the user's server if necessary
        if not hubauth.notebook_server_exists(username):
            return redirect('/hub/home')

        if is_file_request:
            redirection = download_file_and_redirect(
                username=username,
                file_url=args['file'],
                config=current_app.config,
            )
        else:
            redirection = pull_from_github(
                username=username,
                repo_name=args['repo'],
                paths=args['path'],
                config=current_app.config,
            )

        return redirection


@current_app.route('/progress/<string:username>')
def progress(username):
    """Page containing progress on server's running process."""
    return render_template('progress.html')


@current_app.route('/done')
def done():
    """Page containing information about completed process."""
    return 'done'
