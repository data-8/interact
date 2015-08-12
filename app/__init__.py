"""Application body"""
import os
from urllib.request import urlopen
from flask import Flask, redirect
from webargs import Arg
from webargs.flaskparser import use_args


def create_app(config='production'):
	
	app = Flask(__name__)
	
	print(' * Running in {} mode'.format(config))
	app.config.from_object('app.config.%sConfig' % config.capitalize())
	
	args = {
		'file': Arg(str, required=True),
	    'destination': Arg(str)  # must include filename /path/to/file.ipynb
	                             # relative to the directory specified in config
	}
	
	@app.route(app.config['URL'])
	@use_args(args)
	def view(args):
		"""URL to access"""
		redirect_url, username = authenticate()
		if username:
			file_contents = urlopen(args['file']).read()
			destination = os.path.join(
				app.config['COPY_PATH'].format(username=username),
				args['destination'])
			assert '.' in destination and \
				destination.split('.')[-1] in app.config['ALLOWED_FILETYPES']
			open(destination, 'w').write(file_contents)
			redirect_url = app.config['REDIRECT_PATH'].format(path=args['destination'])
		return redirect(redirect_url)
			
	return app


def authenticate():
	"""Authenticates the user with the local JupyterHub installation"""
	return None, None