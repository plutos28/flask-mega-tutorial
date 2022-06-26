from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user

from app import flask_app
from app.forms import LoginForm
from app.models import User


@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {"username": "Victor"}
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
    return render_template("index.html", title="Home", user=user, posts=posts)


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
        # on success, login the user and go to homepage
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))

    return render_template("login.html", title="Sign In", form=form)