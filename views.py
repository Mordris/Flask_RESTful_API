from flask import render_template, redirect, url_for, flash
from app import app, db
from forms import RegistrationForm, LoginForm
from models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    return "Welcome to the Flask app!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('profile'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    return "Welcome to your profile!"


@app.route('/protected')
@login_required
def protected():
    return "WOW! You can see this because you're logged in!"

