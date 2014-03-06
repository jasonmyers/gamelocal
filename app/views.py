# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template

from app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
