from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashboard import Dash_App3

@blueprint.route('/demo')
@login_required
def app1_template():
    return render_template('analytic_app.html', dash_url = Dash_App3.url_base)

    
