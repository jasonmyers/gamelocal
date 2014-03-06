# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask
from flask.ext.babel import Babel

# App
app = Flask(__name__)
app.config.from_object('config')


# Extensions
babel = Babel(app)


# Views
from app import views
