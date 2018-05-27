from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=3, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=2, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=15)])
    username = StringField('Username', [validators.Length(min=4, max=15)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    acclevel = 0
