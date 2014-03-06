# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views
