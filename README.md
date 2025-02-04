# Flask Gentelella

[Gentelella](https://github.com/puikinsh/gentelella) is a free to use Bootstrap admin template.

- [Online demo](https://colorlib.com/polygon/gentelella/)

![Gentelella Bootstrap Admin Template](https://cdn.colorlib.com/wp/wp-content/uploads/sites/2/gentelella-admin-template-preview.jpg "Gentelella Theme Browser Preview")

This project integrates Gentelella with Flask using: 
- [Blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) for scalability.
- [flask_login](https://flask-login.readthedocs.io/en/latest/) for the login system (passwords hashed with bcrypt).
- [flask_migrate](https://flask-migrate.readthedocs.io/en/latest/).
- [dash](https://dash.plot.ly/).

This example's template created by [afourmy](https://github.com/afourmy/flask-gentelella) implemented using Flask-Gentelella.

##  Install requirements 
    pipenv sync
    or
    pip install -r requirements.txt

### Run the application
    (pipenv run) python run.py
    or 
    (pipenv run) sh run_web.sh

### Default Admin User
    username: admin
    password: admin