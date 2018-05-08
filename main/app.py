from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import *
from random import *
import time
from functools import wraps
from forms import *

# Init the application
app = Flask(__name__)
port = 5000

# Routes


@app.route('/')
def index():
    name = 'David'
    return render_template('index.html', **locals())


@app.route('/articles')
def articles():
        # TODO: build articles.html
    return render_template('articles.html')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = "random_large_int"
Bootstrap(app)


@app.route('/login', methods=['GET', 'POST'])  # Step 1 = Methods
def login():
    form = LoginForm()

    if request.method == 'POST':  # Step 2 = If POST is the type of request
        print('Success signing in {}'.format(form.email.data))
        return redirect(url_for('index'))

    return render_template('login.html', **locals())


# Run the server
app.run(port=port)
# test
