# DS8-Interact
side server for UC Berkeley DS8's JuypterHub deployment to copy remote notebooks into user accounts

# Getting Started

1. Create virtual environment `python3 -m venv env`.
2. Activate it. `source env/bin/activate`.
3. Install `pip install -r requirements.txt`.
4. Launch `python3 run.py`.
5. Test `py.test tests`.

# Testing

Use `py.test tests`, or to see it in action:
 
1. From `remote` start a new http server `python -m http.server`.
2. Visit `http://localhost:8002?file=http://localhost:8000/test.json&destination=test.ipynb`
3. You will be redirected to the file on server; your browser may download 
instead of serving it.

# Deploying

Configurations are in `app/config.py`. Modify attributes accordingly in 
`ProductionConfig`.