# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import timedelta

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = os.environ.get('FLASK_DEBUG', True)

ADMINS = ()
SECRET_KEY = os.environ['FLASK_SECRET_KEY']  # Required
REMEMBER_COOKIE_DURATION = timedelta(days=30)
REMEMBER_COOKIE_SECONDS = REMEMBER_COOKIE_DURATION.total_seconds()

PASSWORD_RESET_SECONDS = timedelta(hours=1).total_seconds()

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'FLASK_DATABASE_URL',
    'sqlite:///' + os.path.join(BASEDIR, 'local.db')
)
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.environ.get('FLASK_CSRF_SESSION_KEY')

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = os.environ.get('FLASK_RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('FLASK_RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_OPTIONS = {'theme': 'white'}

LANGUAGES = ['ja', 'en']

if not DEBUG:
    SERVER_NAME = 'gamelocal.net'

SITE_NAME = 'gamelocal'
