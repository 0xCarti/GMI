import os
from os import listdir
from os.path import isfile, join

import flask
from flask import Flask, redirect, render_template, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from instance.models import db, login, UserModel

phone_verification_codes = {}
user_signup_codes = {}
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'avif'}
app = Flask(__name__)
app.secret_key = 'Smkc01002dazzxqn3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if flask.request.method == 'POST':
        return redirect('/login')
    else:
        return render_template('public/signup.html')


@app.route('/', methods=['POST', 'GET'])
@login_required
def home():  # put application's code here
    if current_user.is_authenticated:
        return redirect(f'/profile/{current_user.username}')
    else:
        return redirect('/login')



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
                return render_template('authenticated/user/profile.html', profile_user=profile_user, session_user=current_user, code=code)
        return render_template('public/error.html')


@app.route('/code', methods=['POST'])
@login_required
def code():
    if flask.request.method == 'POST':
        username = flask.request.json['username']
        code = flask.request.json['code']
        user_signup_codes[username] = code
        return redirect('/profile/' + username)
    return redirect('/error')


@app.route('/artwork/<file>', methods=['POST', 'GET'])
@app.route('/artwork', methods=['POST', 'GET'], defaults={'file': ''})
@login_required
def artwork(file: str):
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/audio/<file>', methods=['POST', 'GET'])
@app.route('/audio', methods=['POST', 'GET'], defaults={'file': ''})
@login_required
def audio(file: str):
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/messages/<username>', methods=['POST', 'GET'])
@app.route('/messages', methods=['POST', 'GET'], defaults={'username': ''})
@login_required
def messages(username: str):
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/carts', methods=['POST', 'GET'])
@login_required
def carts():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/bistrowheel', methods=['POST', 'GET'])
@login_required
def bistrowheel():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/bucketlist', methods=['POST', 'GET'])
@login_required
def bucketlist():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/gingerwax-gpt', methods=['POST', 'GET'])
@login_required
def gingerwax_gpt():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/resources', methods=['POST', 'GET'])
@login_required
def resources():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/documentation', methods=['POST', 'GET'])
@login_required
def documentation():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            return  'no file part'
            #return redirect(url_for(f'profile/{current_user.username}', failure_popup="no file part"))
        file = flask.request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'no file name'
            #return redirect(url_for(f'profile/{current_user.username}', failure_popup="no file name"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if 'image' in file.content_type:
                file.save(os.path.join('static/images/artwork', filename))
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'success'
            #return redirect(url_for(f'profile/{current_user.username}', success_popup="Upload Successful"))
    elif flask.request.method == 'GET':
        pass  # render upload page


@app.route('/database', methods=['POST', 'GET'])
def database():
    mode = flask.request.args.get('func')
    if mode == 'init-dev-users':
        user = UserModel(username='0xCarti', admin=True, active=True)
        user.set_password('Snotsuh1')
        db.session.add(user)
        db.session.commit()
        return redirect('/login')


@app.route('/error', methods=['POST', 'GET'])
def error():
    artwork_paths = [f for f in listdir('static/images/artwork') if isfile(join('static/images/artwork', f))]
    return render_template('authenticated/artwork.html', artwork_paths=artwork_paths)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42069, debug=True)

