# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess
import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from app import app, db

from tests.utils import seed_database

UPDATE_COMMAND = 'alembic revision --autogenerate'

UPGRADE_COMMAND = 'alembic upgrade'

DOWNGRADE_COMMAND = 'alembic downgrade'


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


def update(message=''):
    update_command = UPDATE_COMMAND.split()
    if message:
        update_command += ['-m', message]
    print "Running {}".format(' '.join(update_command))
    subprocess.check_call(update_command)


def upgrade(revision=''):
    upgrade_command = UPGRADE_COMMAND.split()
    if revision:
        upgrade_command += [revision]
    print "Running {}".format(' '.join(upgrade_command))
    subprocess.check_call(upgrade_command)


def downgrade(revision=''):
    downgrade_command = DOWNGRADE_COMMAND.split()
    if revision:
        downgrade_command += [revision]
    print "Running {}".format(' '.join(downgrade_command))
    subprocess.check_call(downgrade_command)
