# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from app import app, db

from tests.utils import seed_database


def reset():
    local_db = os.path.join(BASEDIR, 'local.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + local_db

    print "Dropping local database"

    db.drop_all()

    print "Creating new local database"

    db.create_all()

    print "Seeding local database with initial data"

    seed_database(local_db)
