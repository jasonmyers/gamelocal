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
    command = UPDATE_COMMAND.split()
    if message:
        command += ['-m', message]
    print "Running {}".format(' '.join(command))
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass

    print "Revision plans stored in alembic/versions/"


def upgrade(revision='', execute=False):
    command = UPGRADE_COMMAND.split()
    if revision:
        command += [revision]
    if not execute:
        command += ['--sql']
    print "Running {}".format(' '.join(command))
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass
    else:
        if not execute:
            print "   Run again with --execute to execute the above statements"


def downgrade(revision='', execute=False):
    command = DOWNGRADE_COMMAND.split()
    if revision:
        command += [revision]
    if not execute:
        command += ['--sql']
    print "Running {}".format(' '.join(command))
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError:
        pass
    else:
        if not execute:
            print "   Run again with --execute to execute the above statements"
