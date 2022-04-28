from flask import render_template

from app import flask_app

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