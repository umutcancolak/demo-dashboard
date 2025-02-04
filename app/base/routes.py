from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from ..extensions import db, login_manager
from . import blueprint
from .forms import LoginForm, CreateAccountForm
from .models import User


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


# @blueprint.route('/<template>')
# @login_required
# def route_template(template):
#     return render_template(template + '.html')


@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

## Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if user.checkpw(request.form['password']):
                login_user(user)
                return redirect(url_for('home_blueprint.index'))
            else:
                status = 'Password Error !'
        else:
            status = "User doesn't exist !"
        return render_template('login/login.html', login_form = login_form, status = status)

    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    return render_template('login/login.html', login_form = login_form, status = '')
   
@blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    signin_form = CreateAccountForm(request.form)
    if 'signin' in request.form:
        user = User.query.filter_by(username=request.form['username']).first()
        email = User.query.filter_by(email=request.form['email']).first()
        if user :
            status = 'Username is existing'
        elif email:
            status = 'Email is existing'
        else:
            User(**request.form).add_to_db()
            status = 'Add user success !'
        return render_template('login/signin.html', login_form = signin_form, status = status)
    return render_template('login/signin.html', login_form = signin_form, status ="")




@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
