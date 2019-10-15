from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashboard import Dash_Sensors

@blueprint.route('/sensors')
@login_required
def app2_template():
    return render_template('sensors.html', dash_url = Dash_Sensors.url_base)