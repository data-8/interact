import os

def chown(username, path, destination):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, destination), s.st_uid, s.st_gid)

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)
