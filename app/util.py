import os
import shutil
import subprocess
import logging

def chown(path, filename):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, filename), s.st_uid, s.st_gid)

def chown_dir(directory, username):
    """Set owner and group of directory to username."""
    for root, dirs, files in os.walk(directory):
        for child in dirs + files:
            shutil.chown(os.path.join(root, child), username, username)
    logger.info("{} chown'd to {}".format(directory, username))

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)

# Log all messages by default
logging.basicConfig(format='[%(asctime)s]: %(levelname)s -- %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger('app')
