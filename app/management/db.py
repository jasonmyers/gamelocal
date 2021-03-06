# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
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

LOCAL_DATABASE_PATH = os.path.join(BASEDIR, 'local.db')


def delete_pyc_files(path):
    for pyc in glob.glob(
        os.path.join(BASEDIR, os.path.join(*path), '*.pyc')
    ):
        os.remove(pyc)


def reset(clean=False, head=False):
    local_db = os.path.join(BASEDIR, 'local.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + LOCAL_DATABASE_PATH

    delete_pyc_files(['alembic', 'versions'])

    print "Dropping local database"

    try:
        os.remove(LOCAL_DATABASE_PATH)
    except OSError:
        pass

    print "Creating new local database"

    db.create_all()

    if head:
        print "Bumping alembic revision to head"

        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(os.path.join(BASEDIR, 'alembic.ini'))
        command.stamp(alembic_cfg, 'head')

    if not clean:
        print "Seeding local database with initial data"

        seed_database(local_db)


def update(message=''):
    delete_pyc_files(['alembic', 'versions'])
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
    delete_pyc_files(['alembic', 'versions'])
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
    delete_pyc_files(['alembic', 'versions'])
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
