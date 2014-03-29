# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, Blueprint, request, url_for, redirect, \
    flash
from flask.ext.babel import gettext as _
from flask.ext.login import login_user, logout_user, login_required

from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.communications.email import send_email
from app.users.forms import LoginForm, RegisterForm, ResetPasswordForm
from app.users.models import User
from app.users.security import allow_password

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """ Display a password reset form.  Usual entry point is via a link sent
    to the user after pressing 'forgot password'.

    A `User` auth token is required for both 'GET' (via `?token=`) and 'POST'
    (via hidden field on the form, which is populated from the 'GET')

    If the token is missing or invalid in either case, we redirect back to
    the login screen.

    The token expires after `app.config['PASSWORD_RESET_SECONDS']` or once
    the user successfully logs in.
    """
    form = ResetPasswordForm(request.form)

    token = request.args.get('token')
    if token:
        form.token.data = token
    else:
        token = request.form.get('token')

    if not token:
        flash(_('Bad token.'))
        return redirect(url_for('users.login'))

    user = User.from_auth_token(
        token, max_age=app.config['PASSWORD_RESET_SECONDS']
    )
    if not user:
        flash(_('Bad token.'))
        return redirect(url_for('users.login'))

    if form.validate_on_submit():
        new_password = generate_password_hash(form.password.data)
        user.password = new_password
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)

        flash(_('Your password has been changed.'))
        return redirect(url_for('home'))

    return render_template('users/reset_password.html', form=form)


def forgot_password():
    """ No route, as this is triggered from the `login` view, if the user
    presses the 'forgot password' button
    """
    form = LoginForm(request.form)

    form.validate_on_submit()  # Trigger email validation

    if form.email.errors:
        form.password.errors = ()  # Ignore password field for forgot-password
    else:
        email = form.email.data

        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)

        # Don't notify whether we found a user, to prevent fishing for valid
        # email addresses
        flash(_(
            'An email has been sent with '
            'instructions for resetting your password'
        ))

        form = LoginForm()  # Reset the form

    return render_template('users/login.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # Pressed 'forgot password' button
    if 'forgot_password' in request.form:
        return forgot_password()

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                after_login = request.args.get('next') or url_for('home')
                return redirect(after_login)

        form.password.errors = (_("Invalid email or password"),)

    # Ambiguate which field has the error
    if form.email.errors or form.password.errors:
        form.email.errors = (_("Invalid email or password"),)
        form.password.errors = ()

    return render_template('users/login.html', form=form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            form.email.errors = (_('This email is already taken'),)

        elif not allow_password(form.password.data):
            form.password.errors = (_(
                'Your password must contain at least 8 '
                '(printable) characters.'
            ),)

        else:
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data,
            )

            user.set_geo_from_ip(request.remote_addr)

            user.locale = request.accept_languages.best_match(
                app.config['LANGUAGES']
            )

            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)

            send_confirmation_email(user)

            flash(_('An email has been sent to you with a confirmation link. '
                    'Please login to your email at your convenience '
                    'and click the link to finish registration.'))

            return redirect(url_for('home'))

    return render_template('users/register.html', form=form)


@blueprint.route('/confirm_email')
def confirm_email():

    token = request.args.get('token')

    if not token:
        flash(_('Bad token.'))
        return redirect(url_for('home'))

    user = User.from_auth_token_perm(token)

    if not user:
        flash(_('Bad token.'))
        return redirect(url_for('home'))

    User.query.filter_by(id=user.id).update({
        'email_confirmed': True,
    })
    db.session.commit()

    flash(_('Your email has been confirmed, thank you!'))

    return redirect(url_for('home'))


def send_confirmation_email(user):
    send_email(
        to=user.email,
        subject='{site} {subject}'.format(
            site=app.config['SITE_NAME'],
            subject=_('email confirmation'),
        ),
        html=render_template(
            'communications/confirm_email.html',
            user=user,
            app=app,
            token=user.get_auth_token_perm(),
        ),
    )


def send_password_reset_email(user):
    send_email(
        to=user.email,
        subject='{site} {subject}'.format(
            site=app.config['SITE_NAME'],
            subject=_('password reset request'),
        ),
        html=render_template(
            'communications/password_reset_email.html',
            user=user,
            app=app,
            token=user.get_auth_token(),
        ),
    )

