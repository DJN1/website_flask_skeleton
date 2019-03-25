from flask import Flask, flash, redirect, render_template, request, session,\
      url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, \
    logout_user, current_user
import pygal
from pygal.style import NeonStyle
from forms import LoginForm, RegistrationForm, ArticleForm
# import sqlite3
from passlib.hash import sha256_crypt
# from data import Articles

# Init the application
app = Flask(__name__)
port = 5000


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = "random_large_int"
Bootstrap(app)

DATABASE = 'database.db'


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db


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
    acclevel = db.Column(db.Integer, server_default=db.FetchedValue())


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    body = db.Column(db.String)
    create_date = db.Column(db.String, server_default=db.FetchedValue())

# Articles = Articles()


@app.route('/index')
def index():
    return render_template('index.html', **locals())


@app.route('/')
def index1():
    return render_template('index.html')


@app.route('/articles')
def articles():
    listOfArticles = Articles.query.all()

    if len(listOfArticles) > 0:
        return render_template('articles.html', articles=listOfArticles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    return render_template('articles.html', articles=Articles)


@app.route('/article/<string:id>/')
def article(id):
    # Get article
    article = Articles.query.filter_by(id=id).first()
    print(article.create_date)
    date = article.create_date[:10]
    time = article.create_date[10:]
    return \
        render_template('article.html', article=article, date=date, time=time)


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/polls')
def polls():
    pie_chart = pygal.Pie(style=NeonStyle)
    pie_chart.add('First Chart', 1)
    pie_chart.add('First Chart', 3)
    pie_chart.add('First Chart', 0.4)
    pie_chart = pie_chart.render_data_uri()
    return render_template('polls.html', pie_chart=pie_chart)


@app.route('/login', methods=['GET', 'POST'])  # Step 1 = Methods
def login():
    form = LoginForm()
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        user = Users.query.filter_by(email=email).first()
        print(user)
        # Get user by email
        if user is not None and email is not None:
            # Get user password
            password = user.password
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # If password matches, authenticate
                login_user(user, remember=False)
                flash('You are now logged in', 'success')
                print(current_user.username)
                return redirect(url_for('dashboard'))
            else:
                # If invalid password, return invalid login
                error = 'Invalid login'
                flash(error, 'danger')
                return redirect(url_for('login'))
        else:
            # If user not existent, return error
            error = 'Email can\'t be blank'
            flash(error, 'danger')
            return render_template('login.html', error=error)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.first_name.data
        lastname = form.last_name.data
        eMail = form.email.data
        userName = form.username.data
        passWord = sha256_crypt.encrypt(str(form.password.data))
        # Add user
        user = Users(first_name=firstname, last_name=lastname,
                     email=eMail, username=userName, password=passWord)
        db.session.add(user)
        # Commit to DB
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.acclevel == 1:
        adminlistOfArticles = Articles.query.all()
        return render_template('dashboard.html', articles=adminlistOfArticles)
    else:
        listOfArticles = \
            Articles.query.filter_by(author=current_user.username).all()
        return render_template('dashboard.html', articles=listOfArticles)

# Add Article


@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        artTitle = form.title.data
        artBody = form.body.data
        uname = current_user.username

        # Execute query
        newArticle = Articles(title=artTitle, author=uname,
                              body=artBody)
        db.session.add(newArticle)
        # Commit to DB
        db.session.commit()
        flash('Article added successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    # Get article by id
    article = Articles.query.filter_by(id=id).first()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article.title
    form.body.data = article.body

    if request.method == 'POST' and form.validate():
        title = ArticleForm(request.form).title.data
        body = ArticleForm(request.form).body.data
        article.title = title
        article.body = body
        db.session.commit()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)


@app.route('/delete_article/<string:id>', methods=['POST'])
@login_required
def delete_article(id):
    # Query article by id
    article = Articles.query.filter_by(id=id).first()
    print(article)
    # Delete querried article
    db.session.delete(article)
    # Commit to db
    db.session.commit()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    print('Logged out ?', current_user.email)
    session.pop('login', None)
    logout_user()
    return redirect(url_for('index'))


# Run the server
app.run(port=port)
# test
