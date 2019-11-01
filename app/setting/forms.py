from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, SelectField

## login and registration


class add_user_Form(FlaskForm):
    username = TextField('Username', id='username_create')
    email = TextField('Email')
    password = PasswordField('Password', id='pwd_create')

class delete_user_Form(FlaskForm):
    username = TextField('Username', id='username_delete')

class setting_password_Form(FlaskForm):
    username = TextField('Username', id='username_setting')
    password = PasswordField('Password', id='pwd_setting')

class change_password_Form(FlaskForm):
    origin_password = PasswordField('Type Origin Password', id='origin_assword')
    new_password = PasswordField('Type New Password', id='new_assword')
    new_password2 = PasswordField('Type New Password Again', id='new_assword2')

class add_field_Form(FlaskForm):
    field_name = TextField('Type Field Name', id='field_name')

class delete_field_Form(FlaskForm):
    field_name = SelectField(
        'Select Field Name',
        id='field_name',
        coerce=str
        ) 

class add_sensor_Form(FlaskForm):
    field_name = SelectField(
        'Select Field Name',
        id='field_name',
        coerce=str
        )
    sensor_name = SelectField(
        'Select Sensor Type', 
        id='field_name',
        choices=[('valve','Valve'),('observer','Observer')]
        )

class delete_sensor_Form(FlaskForm):
    device_id = SelectField(
        'Select Sensor ID',
        id='sensor_id',
        coerce=str
        )
