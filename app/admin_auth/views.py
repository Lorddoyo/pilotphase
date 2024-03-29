from flask import render_template, redirect, url_for, flash, request
from . import admin_auth
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers, expose

@expose('/login/', methods=('GET', 'POST'))
def login_view(self):
    # handle user login
    form = LoginForm(request.form)
    if helpers.validate_form_on_submit(form):
        user = form.get_user()
        login.login_user(user)

    if login.current_user.is_authenticated:
        return redirect(url_for('.index'))
    link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
    self._template_args['form'] = form
    self._template_args['link'] = link
    return super(MyAdminIndexView, self).index()

@expose('/register/', methods=('GET', 'POST'))
def register_view(self):

    form = RegistrationForm(request.form)
    if helpers.validate_form_on_submit(form):
        user = User()

        form.populate_obj(user)
        # we hash the users password to avoid saving it as plaintext in the db,
        # remove to use plain text:
        user.password = generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()

        login.login_user(user)
        return redirect(url_for('.index'))
    link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
    self._template_args['form'] = form
    self._template_args['link'] = link
    return super(MyAdminIndexView, self).index()

@expose('/logout/')
def logout_view(self):
    login.logout_user()
    return redirect(url_for('.index'))
