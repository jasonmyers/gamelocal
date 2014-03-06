# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, request, g

from app import app, babel


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@babel.localeselector
def get_locale():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
