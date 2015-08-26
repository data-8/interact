"""Application body"""
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from app.auth import HubAuth
from flask import Flask, redirect
from webargs import Arg
from webargs.flaskparser import use_args


def create_app(config='production'):
	
	app = Flask(__name__, static_url_path='/static')
	
	print(' * Running in {} mode'.format(config))
	app.config.from_object('app.config.%sConfig' % config.capitalize())
	
	index_args = {
		'file': Arg(str, required=True)
	}
	
	@app.route(app.config['URL'])
	@use_args(index_args)
	def view(args):
		"""URL to access"""
		try:
			redirection = username = authenticate()
			if isinstance(username, str):
				f = open('/tmp/i.log', 'a')
				f.write('view\n'); f.flush()
				file_contents = get_remote_file(app.config, args['file'])
				f.write('file {}\n'.format(args['file'])); f.flush()
				destination = os.path.basename(args['file'])
				f.write('destination {}\n'.format(destination)); f.flush()
				path = construct_path(app.config['COPY_PATH'], locals())
				f.write('path {}\n'.format(path)); f.flush()
				destination = write_to_destination(file_contents, path, destination, app.config)
				f.write('destination {}\n'.format(destination)); f.flush()
				#print(' * Wrote {}'.format(path + '/' + destination))
				chown(username, path, destination)
				f.write('chowned: {} {} {}\n'.format(username, path, destination)); f.flush()
				redirect_url = construct_path(app.config['REDIRECT_PATH'], locals())
				redirection = redirect(redirect_url)
		except HTTPError:
			return 'Source file "{}" does not exist or is not accessible.'.\
				format(args['file'])
		return redirection
	
	return app

def chown(username, path, destination):
	'''Set owner and group of file to that of the parent directory.'''
	s = os.stat(path)
	os.chown(os.path.join(path, destination), s.st_uid, s.st_gid)

def authenticate():
	"""Authenticates the user with the local JupyterHub installation"""
	return HubAuth().authenticate()

def get_remote_file(config, source):
	"""fetches remote file"""
	assert source.startswith(config['ALLOWED_DOMAIN'])
	return urlopen(source).read().decode('utf-8')

def write_to_destination(file_contents, path, destination, config):
	"""Write file to destination on server"""
	
	f = open('/tmp/w.log', 'a')
	f.write('about to assert\n'); f.flush()
	# check that this filetype is allowed (ideally, not an executable)
	assert '.' in destination and \
		destination.split('.')[-1] in config['ALLOWED_FILETYPES']
	f.write('asserted\n'); f.flush()
	
	if os.path.exists(os.path.join(path, destination)):
		f.write('exists\n'); f.flush()
		root = destination.rsplit('.', 1)[0]
		f.write('root {}\n'.format(root)); f.flush()
		suffix = destination.split('.')[-1]
		f.write('suffix {}\n'.format(suffix)); f.flush()
		destination = '{}-copy.{}'.format(root, suffix)
		f.write('destination {}\n'.format(destination)); f.flush()
		return write_to_destination(file_contents, path, destination, config)

	f.write('about to makedir {}\n'.format(path)); f.flush()
	# make user directory if it doesn't exist
	os.makedirs('/'.join(path.split('/')[:-1]), exist_ok=True)
	f.write('about to write {} {}\n'.format(path, destination)); f.flush()
	
	# write the file
	try:
		open(os.path.join(path, destination), 'w').write(file_contents.encode('utf-8'))
	except Exception as e:
		f.write('EXCEPTION\n'); f.flush()
		f.write(str(e)); f.flush()
		raise e
		
	f.write('wrote\n'); f.flush()
	return destination
	
def construct_path(path, format, *args):
	"""constructs a path using locally available variables"""
	return os.path.join(path.format(**format), *args)
