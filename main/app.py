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

DATABASE = 'database.db'


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
    cur = get_db().cursor()
    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = ?", [id])
    article = cur.fetchone()
    return render_template('article.html', article=article)


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
    form = LoginForm()
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        # Create cursor
        cur = get_db().cursor()
        # Get user by email
        cur.execute("SELECT * FROM users WHERE email = ?", [email])
        result = cur.fetchone()
        print(cur.fetchone())
        if result is not None:
            # Get stored hash
            cur.execute("SELECT * FROM users WHERE email = ?", [email])
            data = cur.fetchone()
            print(data)
            password = data[5]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html', form=form)


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
        print(cur.execute('''SELECT * FROM users''').fetchone())
        cur.execute(
            'INSERT INTO users(first_name, last_name, email, username, password) VALUES(?, ?, ?, ?, ?)', (first_name, last_name, email, username, password))

        # Commit to DB
        get_db().commit()
        cur.close()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))

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
app.run(port=port)
# test
