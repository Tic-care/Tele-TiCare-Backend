from flask import request, jsonify ,render_template, redirect, url_for, flash
from ticare import app, ALLOWED_EXTENSIONS , db
from ticare.models import User ,Session
from ticare.forms import RegisterForm, LoginForm
from ticare.functions import preprocesss
from flask_login import login_user

import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/sessions')
def session_page():
    Sessions = Session.query.all()
    print(Sessions)
    return render_template('sessions.html', Sessions=Sessions)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'})

    video_file = request.files['video']

    if video_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if video_file and allowed_file(video_file.filename):
        filename = f'recorded{app.config["COUNT"]}.webm'
        app.config['COUNT'] += 1  # Increment the counter for the next file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(filepath)
        preprocesss(filepath)

        return jsonify({'message': 'Video uploaded successfully'})

    return jsonify({'error': 'Invalid file format'})
