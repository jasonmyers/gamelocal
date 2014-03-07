# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from flask import Flask

# App
app = Flask(__name__)
app.config.from_object('config')


# Extensions
from flask.ext import babel, assets, sqlalchemy

db = sqlalchemy.SQLAlchemy(app)

babel = babel.Babel(app)

webassets = assets.Environment(app)

# In the future, we may set this to False and build assets before deployment.
# Build has a minor cost in Production, so we'll optimize this when we need to
# noqa See http://elsdoerfer.name/docs/webassets/environment.html#webassets.env.Environment.auto_build
webassets.auto_build = True

webassets.register(
    'js_app',
    assets.Bundle(
        # Add new .js files here
        # 'js/lib.js',
        assets.Bundle(
            # Add new .coffee files here
            'js/main.coffee',
            filters='coffeescript',
            output='compiled/main.js',
        ),
        filters='rjsmin',
        output='compiled/app.js',
    )
)

webassets.register(
    'css_app',
    assets.Bundle(
        # Add new .css files here
        'css/reset.css',
        assets.Bundle(
            # Add new .scss files here
            'css/main.scss',
            filters='scss',
            output='compiled/main.css',
        ),
        filters='cssmin',
        output='compiled/app.css',
    )
)

# Views
from app import views
