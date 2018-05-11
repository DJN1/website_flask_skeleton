from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
