from . import blueprint
from flask import render_template, current_app, request, redirect
from flask_login import login_required, current_user
from .forms import (
    add_user_Form, 
    delete_user_Form, 
    change_password_Form, 
    setting_password_Form, 
    add_field_Form,
    add_sensor_Form
    )
from ..base.models import User, FieldInformationModel, SensorInformationModel

@blueprint.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_User():
    admin_user = current_app.config['ADMIN']['username']
    if current_user.username == admin_user: 
        form = add_user_Form(request.form)
        if 'Add' in request.form:
            user = User.query.filter_by(username=request.form['username']).first()
            email = User.query.filter_by(email=request.form['email']).first()
            if user :
                status = 'Username is existing'
            elif email:
                status = 'Email is existing'
            else:
                User(**request.form).add_to_db()
                status = 'Add user success !'
            return render_template('add_user.html', form = form, status = status)
        return render_template('add_user.html', form = form, status = '')
    return redirect('/page_403')

@blueprint.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():    
    admin_user = current_app.config['ADMIN']['username']
    if current_user.username == admin_user:  
        form = delete_user_Form(request.form)
        if 'Delete' in request.form:
            username = request.form['username']
            user = User.query.filter_by(username=username).first()
            if user:
                if username == admin_user: 
                    status = "admin user can't be deleted !"
                else:
                    user.delete_from_db()
                    status = "delete user success !"
            else:
                status = "user doesn't exist !"
            return render_template('delete_user.html', form = form, status = status)
        return render_template('delete_user.html', form = form, status = '') 
    return redirect('/page_403')

@blueprint.route('/setting_password', methods=['GET', 'POST'])
@login_required
def setting_password():
    admin_user = current_app.config['ADMIN']['username']
    if current_user.username == admin_user:  
        form = setting_password_Form(request.form)
        if 'Setting' in request.form:
            username = request.form['username']
            user = User.query.filter_by(username=username).first()
            if user:
                if username == admin_user: 
                    status = "please change admin password from server !"
                else:
                    user.password = user.hashpw(request.form['password'])
                    user.db_commit()
                    status = "Setting password success !"
            else:
                status = "user doesn't exist !"
            return render_template('setting_password.html', form = form, status = status)
        return render_template('setting_password.html', form = form, status = '') 
    return redirect('/page_403')

@blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    admin_user = current_app.config['ADMIN']['username']
    if current_user.username == admin_user:  
        return 'please change admin password from server'
    else:
        form = change_password_Form(request.form)
        if 'Change' in request.form:
            user = User.query.filter_by(username=current_user.username).first()
            if user.checkpw(request.form['origin_password']):
                if request.form['new_password'] == request.form['new_password2']:
                    user.password = user.hashpw(request.form['new_password'])
                    user.db_commit()
                    status = "Change Password Success !"
                else:
                    status = "Both New Password is Not Equal !"
            else:
                status = "Origin Password Error !"
            return render_template('change_password.html', form = form, status = status)
        return render_template('change_password.html', form = form, status = '')

@blueprint.route('/add_field', methods=['GET', 'POST'])
@login_required
def add_field():
    form = add_field_Form(request.form)
    if 'Add' in request.form:
        admin_user = current_app.config['ADMIN']['username']
        if current_user.username == admin_user: 
            status = "Admin user does not have permission to create field!"
            return render_template('add_field.html', form = form, status = status)
        user = User.query.filter_by(username=current_user.username).first()
        FieldInformationModel(user.id,request.form["field_name"]).save_to_db()        
        status = 'Add field success !'        
        return render_template('add_field.html', form = form, status = status)
    return render_template('add_field.html', form = form, status = '')


@blueprint.route('/add_sensor', methods=['GET', 'POST'])
@login_required
def add_sensor():
    form = add_sensor_Form(request.form)
    if 'Add' in request.form:
        admin_user = current_app.config['ADMIN']['username']
        if current_user.username == admin_user: 
            status = "Admin user does not have permission to create sensor!"
            return render_template('add_sensor.html', form = form, status = status)
        user = User.query.filter_by(username=current_user.username).first()
        if FieldInformationModel.find_by_user_id_and_field_name(user.id, request.form["field_name"]):
            new_sensor = SensorInformationModel(user.id,request.form["field_name"],request.form["sensor_name"])
            new_sensor.save_to_db()
            status = "Add sensor success ! Your device id : {}".format(new_sensor.get_device_id())
            return render_template('add_sensor.html', form = form, status = status)        
        status = 'Add sensor failed ! There is no field name like {}'.format(request.form["field_name"])
        return render_template('add_sensor.html', form = form, status = status)
    return render_template('add_sensor.html', form = form, status = '')