import os
import re

from flask import redirect
import git

from . import util


def pull_from_github(**kwargs):
    """
    Initializes git repo if needed, then pulls new content from Github using
    sparse checkout.

    Redirects the user to the final path provided in the URL. Eg. given a path
    like:

        repo=data8assets&path=labs/lab01&path=labs/lab01/lab01.ipynb

    The user will be redirected to the lab01.ipynb notebook (and open it).

    This pull preserves the original content in case of a merge conflict by
    making a WIP commit then pulling with -Xours.

    It resets deleted files back to their original state before a pull to allow
    getting back the original file more easily.

    Reference:
    http://jasonkarns.com/blog/subdirectory-checkouts-with-git-sparse-checkout/

    Kwargs:
        username (str): The username of the JupyterHub user
        repo_name (str): The repo under the dsten org to pull from, eg.
            textbook or health-connector.
        paths (list of str): The folders and file names to pull.
        config (Config): The config for this environment.
    """
    username = kwargs['username']
    repo_name = kwargs['repo_name']
    paths = kwargs['paths']
    config = kwargs['config']

    assert username and repo_name and paths and config

    util.logger.info('Starting pull.')
    util.logger.info('    User: {}'.format(username))
    util.logger.info('    Repo: {}'.format(repo_name))
    util.logger.info('    Paths: {}'.format(paths))

    repo_dir = util.construct_path(config['COPY_PATH'], locals(), repo_name)

    try:
        if not os.path.exists(repo_dir):
            _initialize_repo(repo_name, repo_dir, config=config)

        _add_sparse_checkout_paths(repo_dir, paths)

        repo = git.Repo(repo_dir)
        _reset_deleted_files(repo)
        _make_commit_if_dirty(repo)

        _pull_and_resolve_conflicts(repo, config=config)

        if config['GIT_REDIRECT_PATH']:
            # Redirect to the final path given in the URL
            destination = os.path.join(repo_name, paths[-1])
            redirect_url = util.construct_path(config['GIT_REDIRECT_PATH'], {
                'username': username,
                'destination': destination,
            })
            util.logger.info('Redirecting to {}'.format(redirect_url))
            return redirect(redirect_url)
        else:
            return 'Pulled from repo: ' + repo_name
    except git.exc.GitCommandError as git_err:
        util.logger.error(git_err)
        return git_err.stderr
    finally:
        # Always set ownership to username in case of a git failure
        # In development, don't run the chown since the sample user doesn't
        # exist on the system.
        if config['MOCK_AUTH']:
            util.logger.info("We're in development so we won't chown the dir.")
        else:
            util.chown_dir(repo_dir, username)

def _initialize_repo(repo_name, repo_dir, config=None):
    """
    Clones repository and configures it to use sparse checkout.
    Extraneous folders will get removed later using git read-tree
    """
    util.logger.info('Repo {} doesn\'t exist. Cloning...'.format(repo_name))
    # Clone repo
    repo = git.Repo.clone_from(config['GITHUB_ORG'] + repo_name, repo_dir,
                               branch=config['REPO_BRANCH'])

    # Use sparse checkout
    config = repo.config_writer()
    config.set_value('core', 'sparsecheckout', True)
    config.release()

    util.logger.info('Repo {} initialized'.format(repo_name))


DELETED_FILE_REGEX = re.compile(
    r"deleted:\s+"  # Look for deleted: + any amount of whitespace...
    r"(\S+)"        # and match the filename afterward.
)
def _reset_deleted_files(repo):
    """
    Runs the equivalent of git checkout -- <file> for each file that was
    deleted. This allows us to delete a file, hit an interact link, then get a
    clean version of the file again.
    """
    git_cli = repo.git
    deleted_files = DELETED_FILE_REGEX.findall(git_cli.status())

    if deleted_files:
        git_cli.checkout('--', *deleted_files)
        util.logger.info('Resetted these files: {}'.format(deleted_files))


def _add_sparse_checkout_paths(repo_dir, paths):
    """
    Runs the equivalent of

    echo /path >> .git/info/sparse-checkout

    for each path in paths but also avoids duplicates.
    """
    sparsecheckout_path = os.path.join(repo_dir,
                                       '.git', 'info', 'sparse-checkout')

    existing_paths = []
    try:
        with open(sparsecheckout_path) as info_file:
            existing_paths = [line.strip().strip('/')
                              for line in info_file.readlines()]
    except FileNotFoundError:
        pass

    util.logger.info(
        'Existing paths in sparse-checkout: {}'.format(existing_paths))

    to_write = [path for path in paths if path not in existing_paths]
    with open(sparsecheckout_path, 'a') as info_file:
        for path in to_write:
            info_file.write('/{}\n'.format(path))

    util.logger.info('{} written to sparse-checkout'.format(to_write))


def _make_commit_if_dirty(repo):
    """
    Makes a commit with message 'WIP' if there are changes.
    """
    if repo.is_dirty():
        git_cli = repo.git
        git_cli.add('-A')
        git_cli.commit('-m', 'WIP')

        util.logger.info('Made WIP commit')


def _pull_and_resolve_conflicts(repo, config=None):
    """
    Git pulls, resolving conflicts with -Xours
    """
    util.logger.info('Starting pull from {}'.format(repo.remotes['origin']))

    git_cli = repo.git

    # Fetch then merge, resolving conflicts by keeping original content
    git_cli.fetch('origin', config['REPO_BRANCH'])
    git_cli.merge('-Xours', 'origin/' + config['REPO_BRANCH'])

    # Ensure only files/folders in sparse-checkout are left
    git_cli.read_tree('-mu', 'HEAD')

    util.logger.info('Pulled from {}'.format(repo.remotes['origin']))
