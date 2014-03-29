# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, request, g
from flask.ext.login import current_user

from app import app, babel, login_manager

from app.users.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@babel.localeselector
def get_locale():
    return (
        current_user.is_authenticated() and current_user.locale or
        request.accept_languages.best_match(app.config['LANGUAGES'])
    )


@babel.timezoneselector
def get_timezone():
    return (
        current_user.is_authenticated() and current_user.timezone or
        None
    )


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
