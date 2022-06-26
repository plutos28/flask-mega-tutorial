from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import flask_app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@flask_app.route("/")
@flask_app.route("/index")
@login_required
def index():
    posts = [
        {
            "author": {"username": "Victor"},
            "body": "Beautiful day in Juba!"
        },
        {
            "author": {"username": "Bird"},
            "body": "Attack on Titan ended horribly."
        },
        {
            "author": {"username": "Johnny Boy"},
            "body": "Damn I love to workout."
        },
    ]
    return render_template("index.html", title="Home", posts=posts)


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Congrutulations {user.username}, you are now a registered user! Sign In Below")
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@flask_app.route("/login", methods=["GET", "POST"])
def login():
    # return to homepage if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if the username is invalid or the password is wrong
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # on success, login the user and go to homepage or the next_page query string argument
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@flask_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))