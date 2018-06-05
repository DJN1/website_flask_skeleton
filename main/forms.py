from wtforms import *
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class RegistrationForm(Form):
    first_name = StringField('First Name', [validators.Length(min=3, max=25)])
    last_name = StringField('Last Name', [validators.Length(min=2, max=40)])
    email = StringField('Email Address', [validators.Length(min=6, max=100)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, max=100)
    ])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])
    acclevel = 0


class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
