"""Application body"""
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from app.auth import HubAuth
from flask import Flask, redirect
from webargs import fields
from webargs.flaskparser import use_args


def create_app(config='production'):

    app = Flask(__name__, static_url_path='/static')

    print(' * Running in {} mode'.format(config))
    app.config.from_object('app.config.%sConfig' % config.capitalize())

    index_args = {
        'file': fields.Str(required=True)
    }

    @app.route(app.config['URL'])
    @use_args(index_args)
    def view(args):
        """
        /?file=file_url

        Authenticates, then downloads file into user's file system.
        """
        try:
            # authenticate() returns either a username as a string or a redirect
            redirection = username = authenticate()

            is_authenticated = isinstance(username, str)
            if is_authenticated:
                file_contents = get_remote_file(app.config, args['file'])
                destination = os.path.basename(args['file'])
                path = construct_path(app.config['COPY_PATH'], locals())

                # destination might change if the file results in a copy
                destination = write_to_destination(
                    file_contents, path, destination, app.config)
                #print(' * Wrote {}'.format(path + '/' + destination))
                chown(username, path, destination)

                redirect_url = construct_path(
                    app.config['REDIRECT_PATH'], locals())
                redirection = redirect(redirect_url)
        except HTTPError:
            return 'Source file "{}" does not exist or is not accessible.'.\
                format(args['file'])

        return redirection

    return app

def chown(username, path, destination):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, destination), s.st_uid, s.st_gid)

def authenticate():
    """Authenticates the user with the local JupyterHub installation."""
    return HubAuth().authenticate()

def get_remote_file(config, source):
    """Fetches file, throws an HTTPError if the file is not accessible."""
    assert source.startswith(config['ALLOWED_DOMAIN'])
    return urlopen(source).read().decode('utf-8')

def write_to_destination(file_contents, path, destination, config):
    """Write file to destination on server."""

    # check that this filetype is allowed (ideally, not an executable)
    assert '.' in destination and \
        destination.split('.')[-1] in config['ALLOWED_FILETYPES']

    if os.path.exists(os.path.join(path, destination)):
        root = destination.rsplit('.', 1)[0]
        suffix = destination.split('.')[-1]
        destination = '{}-copy.{}'.format(root, suffix)
        return write_to_destination(file_contents, path, destination, config)

    # make user directory if it doesn't exist
    os.makedirs('/'.join(path.split('/')[:-1]), exist_ok=True)

    # write the file
    open(os.path.join(path, destination), 'wb').write(file_contents.encode('utf-8'))

    return destination

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)
