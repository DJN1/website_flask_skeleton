from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, flash, jsonify, g, logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
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
import datetime
from functools import wraps
from forms import *
import sqlite3
from passlib.hash import sha256_crypt
from data import Articles

# Init the application
app = Flask(__name__)
port = 5000


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = "random_large_int"
Bootstrap(app)

DATABASE = '/main/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


# def make_dicts(cursor, row):
#     return dict((cursor.description[idx][0], value)
#                 for idx, value in enumerate(row))
#     db.row_factory = make_dicts


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(100))
    username = db.Column(db.String(30))
    password = db.Column(db.String(100))
    register_date = db.Column(db.String, default=str(func.current_timestamp()))
    acclevel = db.Column(db.Integer, default=0)


Articles = Articles()


@app.route('/index')
def index():
    active = 'home'
    return render_template('index.html', **locals())


@app.route('/')
def index1():
    active = 'home'
    return render_template('index.html')


@app.route('/articles')
def articles():
    active = 'articles'
    # TODO: build articles.html
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


@app.route('/team')
def team():
    active = 'team'
    return render_template('team.html')


@app.route('/about')
def about():
    active = 'about'
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])  # Step 1 = Methods
def login():
    active = 'login'
    form = LoginForm()

    if request.method == 'POST':
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                print("Logged {} {} in".format(current_user.first_name,
                                               current_user.last_name))
                return redirect(url_for('dashboard'))
            else:
                print("Something is wrong with this login info...")
                return redirect(url_for('login'))
        else:
            print("This isn't a user...")
            render_template('login.html', **locals())

    return render_template('login.html', **locals())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = get_db().cursor()
        # Add user
        cur.execute(
            "INSERT INTO users(first_name, last_name, email, username, password) VALUES(%s, %s, %s, %s, %s)", (first_name, last_name, email, username, password))

        # Commit to DB
        db.commit()
        flash('Registered successfully!', 'success')

        # Close connection
        cur.close()
        redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    active = 'dashboard'
    return render_template('dashboard.html', **locals())


@app.route('/logout')
@login_required
def logout():
    active = 'logout'
    print('Logged out {}'.format(current_user.email))
    session.pop('login', None)
    logout_user()
    return redirect(url_for('index'))


# Run the server
# app.run(port=port)
# test
