import os

def chown(username, path, destination):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, destination), s.st_uid, s.st_gid)

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)

def logger(config):
    """ Returns a logger if development mode, else a no-op. """
    def log(message):
        print('[Debug]: {}'.format(message))

    if config['DEBUG']:
        return log
    else:
        return lambda x: None
