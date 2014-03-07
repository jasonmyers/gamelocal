# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ADMINS = ()
SECRET_KEY = os.environ['FLASK_SECRET_KEY']  # Required

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
