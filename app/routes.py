from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import flask_app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

from datetime import datetime


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


@flask_app.route('/user/<username>')
@login_required
def user(username):
    # if the result is None, then 404(resource not found)
    user = User.query.filter_by(username=username).first_or_404() 
    posts = [
        {'author': user, 'body': 'Test post #1'}, 
        {'author': user, 'body': 'Test post #2'}, 
    ]
    return render_template('user.html', user=user, posts=posts)


@flask_app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
    elif request.method == 'GET':
        # on get request, provide original values for editing
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@flask_app.before_request
def before_request():
    # update the last seen value of the user before a request
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
