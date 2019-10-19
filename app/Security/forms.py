from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField

## login and registration

class get_access_token_Form(FlaskForm):
    time = IntegerField('Type Access Token Expiration Time (minutes)', id = 'exp_time')