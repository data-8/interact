

DSTEN_ORG = 'https://github.com/dsten'

def pull_from_github(**kwargs):
    """
    Initializes git repo if needed, then pulls new content from Github.
    This pull preserves the original content in case of a merge conflict.

    Kwargs:
        username (str): The username of the JupyterHub user
        repo (str): The repo under the dsten org to pull from, eg. textbook or
            health-connector.
        paths (list of str): The folders and file names to pull.
        config (Config): The config for this environment.
    """
    username = kwargs['username']
    repo = kwargs['repo']
    paths = kwargs['paths']
    config = kwargs['config']

    assert username and repo and paths and config

    return '{} {}'.format(repo, paths)
