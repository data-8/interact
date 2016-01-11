# DS8-Interact
Side server for UC Berkeley DS8's JuypterHub deployment to copy remote notebooks
into user accounts

# Getting Started

1. Create virtual environment `python3 -m venv env`.
2. Activate it. `source env/bin/activate`.
3. Install `pip install -r requirements.txt`.
4. Launch `python3 run.py`.
5. Test `py.test tests`.

# Testing

Use `py.test tests`, or to see it in action:

1. Run the server `python run.py --development`.
2. From `remote` start another http server `python -m http.server`. This is a
dummy for the remote website, serving example notebooks.
3. Visit `http://localhost:8002/?file=http://localhost:8000/test.ipynb`
4. You will be redirected to the file on server; your browser may download
instead of serving it.
5. The file's contents will match that of remote/test.ipynb

# Deploying

1. Setup in `/var/www/interact`.
2. Configurations are in `app/config.py`. Modify attributes accordingly in
`ProductionConfig`.
3. Run the server `python run.py --production`.
4. Point WSGI to `/var/www/interact/index.wsgi`.
5. Optionally use the *Apache2* configuration file.

WSGI script and Apache configuration file assumes that the program is installed
under `/var/www/interact`.
