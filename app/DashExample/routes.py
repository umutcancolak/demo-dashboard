from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashboard import Dash_App2

@blueprint.route('/app2')
@login_required
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base)