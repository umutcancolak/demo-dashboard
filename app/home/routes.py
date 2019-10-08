from . import blueprint
from flask import render_template
from flask_login import login_required, current_user
from Dashboard import Dash_Home

@blueprint.route('/')
@login_required
def index():
    return render_template('index.html', dash_url = Dash_Home.url_base)

    