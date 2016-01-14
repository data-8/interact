import os
import logging

def chown(path, filename):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, filename), s.st_uid, s.st_gid)

def chown_dir(directory):
    """Set owner and group of directory to that of its parent directory."""
    s = os.stat(os.path.dirname(directory))
    for root, dirs, files in os.walk(directory):
        for child in dirs + files:
            os.chown(os.path.join(root, child), s.st_uid, s.st_gid)

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)

# Log all messages by default
logging.basicConfig(format='[%(asctime)s]: %(levelname)s -- %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger('app')
