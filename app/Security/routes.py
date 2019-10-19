from . import blueprint
from flask import render_template, request, redirect
from flask_login import login_required, current_user
from ..base.models import User
from .forms import get_access_token_Form

from datetime import timedelta
from flask_jwt_extended import create_access_token


@blueprint.route('/jwt_access', methods=['GET', 'POST'])
@login_required
def get_access_token():
    form =  get_access_token_Form(request.form)      
    if "Add" in request.form:
        user = User.query.filter_by(username=current_user.username).first()
        expires = timedelta(minutes=int(request.form["time"]))
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return render_template('get_token.html', form = form, status = access_token)
    return render_template('get_token.html', form = form, status = "")    
