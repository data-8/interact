"""Application body"""
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from flask import Flask, redirect
from webargs import Arg
from webargs.flaskparser import use_args


def create_app(config='production'):
	
	app = Flask(__name__, static_url_path='/static')
	
	print(' * Running in {} mode'.format(config))
	app.config.from_object('app.config.%sConfig' % config.capitalize())
	
	index_args = {
		'file': Arg(str, required=True),
		# must include filename /path/to/file.ipynb relative to the directory 
		# specified in config
	    'destination': Arg(str, required=True)
	}
	
	@app.route(app.config['URL'])
	@use_args(index_args)
	def view(args):
		"""URL to access"""
		try:
			redirection = username = authenticate()
			if isinstance(username, str):
				file_contents = get_remote_file(app.config, args['file'])
				destination = args['destination']
				path = construct_path(app.config['COPY_PATH'], locals())
				write_to_destination(file_contents, path, app.config)
				redirect_url = construct_path(app.config['REDIRECT_PATH'], locals())
				redirection = redirect(redirect_url)
		except HTTPError:
			return 'Source file "{}" does not exist or is not accessible.'.\
				format(args['file'])
		return redirection
	
	return app


def authenticate():
	"""Authenticates the user with the local JupyterHub installation"""
	return None, 'JohnnyAppleseed'


def get_remote_file(config, source):
	"""fetches remote file"""
	assert source.startswith(config['ALLOWED_DOMAIN'])
	return urlopen(source).read().decode('utf-8')


def write_to_destination(file_contents, destination, config):
	"""Write file to destination on server"""
	
	# check that this filetype is allowed (ideally, not an executable)
	assert '.' in destination and \
	       destination.split('.')[-1] in config['ALLOWED_FILETYPES']
	
	# make user directory if it doesn't exist
	os.makedirs('/'.join(destination.split('/')[:-1]), exist_ok=True)
	
	# write the file
	open(destination, 'w').write(file_contents)
	
	
def construct_path(path, format, *args):
	"""constructs a path using locally available variables"""
	return os.path.join(path.format(**format), *args)