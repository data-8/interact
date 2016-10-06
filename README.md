# Interact
Interact is a JupyterHub hub-side service that can import remote notebooks into user accounts.

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

See https://github.com/data-8/jupyterhub-deploy/tree/master/roles/interact.
