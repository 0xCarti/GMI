import json
import secrets
from datetime import datetime

import flask
from flask import Flask, redirect, render_template, url_for
from flask_login import login_required, current_user, login_user, logout_user
from instance.models import db, login, UserModel

phone_verification_codes = {}
user_signup_codes = {}
app = Flask(__name__)
app.secret_key = 'Smkc01002dazzxqn3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
login.init_app(app)
login.login_view = 'login'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'POST':
        signup_code = flask.request.json['code']
        if signup_code not in user_signup_codes.values():
            return 'Invalid signup code.'
        username = flask.request.json['username']
        password = flask.request.json['password']
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return 'Username already taken.'
        user = UserModel(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('public/signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(f'/profile/{current_user.username}')

    if flask.request.method == 'POST':
        username = flask.request.json['username']
        password = flask.request.json['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(f'/profile/{username}')
        else:
            return 'Invalid User or Credentials.'  # make the page display a note for the user, so they know tiw as a fail
    else:
        return render_template('public/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
@login_required
def home():  # put application's code here
    render_template('public/login.html')


@app.route('/profile/<username>', methods=['POST', 'GET'])
@login_required
def profile(username: str):
    if flask.request.method == 'POST':
        if current_user.admin or current_user.username == username:
            username = flask.request.json['username']
            email = flask.request.json['email']
            phone = flask.request.json['phone']
            password = flask.request.json['password']
            admin = flask.request.json['admin']
            activated = bool(flask.request.json['activated'])
            user = UserModel.query.filter_by(username=username).first()
            if user:
                user.username = username
                user.email = email
                user.phone = phone
                user.admin = admin
                user.active = activated
                if password != '':
                    user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return redirect(f'/profile/{username}')
        return 'fail'  # make the page display a note for the user, so they know tiw as a fail
    elif flask.request.method == 'GET':
        if current_user.admin or current_user.username == username:
            profile_user = UserModel.query.filter_by(username=username).first()
            code = ''
            if profile_user.username in user_signup_codes:
                code = user_signup_codes[profile_user.username]
            if profile_user:
                return render_template('authenticated/basic/user/profile.html', profile_user=profile_user, session_user=current_user, code=code)
        return render_template('public/404.html')


@app.route('/code', methods=['POST'])
def code():
    if flask.request.method == 'POST':
        username = flask.request.json['username']
        code = flask.request.json['code']
        user_signup_codes[username] = code
        return redirect('/profile/' + username)
    return redirect('/error')


@app.route('/database', methods=['POST', 'GET'])
def database():
    mode = flask.request.args.get('func')
    if mode == 'init-dev-users':
        user = UserModel(username='0xCarti', admin=True, active=True)
        user.set_password('Snotsuh1')
        db.session.add(user)
        db.session.commit()
        return redirect('/login')


if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5000, debug=True)
