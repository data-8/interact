import os
import subprocess
import logging

def chown(path, filename):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, filename), s.st_uid, s.st_gid)

def chown_dir(directory, username):
    """Set owner and group of directory to username."""
    command = ['chown', '-R', '{u}:{u}'.format(u=username), directory]
    # Throws subprocess.CalledProcessError on error
    subprocess.check_call(command, shell=True)

    logger.info(' '.join(command))

def construct_path(path, format, *args):
    """Constructs a path using locally available variables."""
    return os.path.join(path.format(**format), *args)

# Log all messages by default
logging.basicConfig(format='[%(asctime)s]: %(levelname)s -- %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger('app')
