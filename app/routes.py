from flask import render_template, flash, redirect

from app import flask_app
from app.forms import LoginForm


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
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}, remember me={form.remember_me.data}")
        return redirect("/index")

    return render_template("login.html", title="Sign In", form=form)