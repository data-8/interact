import os
import shutil
import logging

from flask_socketio import emit

"""
Format for downloading zip files of Git folders

:param repo: the repository name, from the Data8 organization on Github
:param path: path to the desired file or folder
"""
GIT_DOWNLOAD_LINK_FORMAT = 'https://minhaskamal.github.io/DownGit/#/home?url' \
                           '=http://github.com/data-8/{repo}/tree/gh-pages/{' \
                           'path}'


def chown(path, filename):
    """Set owner and group of file to that of the parent directory."""
    s = os.stat(path)
    os.chown(os.path.join(path, filename), s.st_uid, s.st_gid)


def chown_dir(directory, username):
    """Set owner and group of directory to username."""
    shutil.chown(directory, username, username)
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


def generate_git_download_link(args):
    """Generates a download link for files hosted on Git.

    :param args: dictionary of query string "arguments"
    :return: URIs for the specified git resources
    """
    return [GIT_DOWNLOAD_LINK_FORMAT.format(
        repo=args['repo'],
        path=path) for path in args['path']]


def emit_estimate_update(tracker):
    """Emit time estimates for each process. Extremely rough.

    This should be a function of the number of processes currently running.
    Broadcasts to all listeners.

    :param tracker: the status to send
    """
    emit(
        'estimate update',
        {'estimate': 30 * len(tracker)},
        broadcast=True,
        namespace='/global')


def emit_status(namespace, status):
    """Emit statuses for client-side progress displays.

    :param namespace: namespace to broadcast status to
    :param status: the status to send
    """
    logger.info('Emit "{status}" to "{namespace}"'.format(
        status=status,
        namespace=namespace))
    emit(
        'status update',
        {'status': status},
        broadcast=True,
        namespace=namespace)


def emit_log(namespace, log):
    """Emit logs for client-side progress displays.

    :param namespace: namespace to broadcast logs to
    :param log: the log contents
    """
    emit(
        'log update',
        {'log': log},
        broadcast=True,
        namespace=namespace)


def emit_and_log(namespace, status):
    """Emit status and log info.

    :param namespace: namespace to broadcast status to
    :param status: the status to send
    """
    logger.info(status)
    emit_status(namespace, status)


def emit_finished(namespace, redirect):
    """Emit the final status update, indicating that the process has finished.

    :param namespace: namespace to broadcast status to
    :param redirect: the url to redirect the user to
    """
    emit(
        'process complete',
        {'url': redirect},
        broadcast=True,
        namespace=namespace)
