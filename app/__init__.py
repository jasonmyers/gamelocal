# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask

# App
app = Flask(__name__)
app.config.from_object('config')

import logging

if app.config['DEBUG']:
    app.logger.setLevel(logging.DEBUG)
else:
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)


# Extensions
from flask.ext import assets, sqlalchemy, login
from flask.ext.babel import Babel, lazy_gettext as _

db = sqlalchemy.SQLAlchemy(app)

babel = Babel(app)

login_manager = login.LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message = _("You must login to view this page.")
login_manager.localize_callback = unicode
login_manager.session_protection = "strong"
from app.users.models import User
login_manager.token_loader(User.from_auth_token)
login_manager.init_app(app)

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
            'js/geo.coffee',
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
            'css/geo.scss',
            filters='scss',
            output='compiled/main.css',
        ),
        filters='cssmin',
        output='compiled/app.css',
    )
)

# Views
from app import views

from app.clubs.views import blueprint as clubs_blueprint
app.register_blueprint(clubs_blueprint)

from app.users.views import blueprint as users_blueprint
app.register_blueprint(users_blueprint)
