from flask import render_template, redirect, url_for, flash, request
from . import user_auth
from ..models import User, Member
from .forms import RegistrationForm, LoginForm
from .. import db
from flask_login import login_user, logout_user, login_required



@user_auth.route('/login', methods = ["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            # user.authenticated = True
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Acess Control login"

    return render_template('user_auth/login.html',login_form = login_form,title=title)

@user_auth.route('/register', methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.subscribe.data:
            member = Member(email = form.email.data, username = form.username.data)
            db.session.add(member)
            db.session.commit()

        return redirect(url_for('user_auth.login'))
        title = "New Account"
    return render_template('user_auth/signup.html',  registration_form = form)

@user_auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    flash('You have been Successfully logged out')
    return redirect(url_for("main.index"))