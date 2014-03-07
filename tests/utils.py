# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from app import app, db

TEST_DATABASE_PATH = os.path.join(BASEDIR, 'test.db')


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Any models to be tested must be imported in the test's
        `setUpClass` method, as they need to be patched prior to
        `db.create_all()` in `setUp`
        """
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + TEST_DATABASE_PATH

    def setUp(self):
        self.app = app.test_client()

        self.context = self.app.application.test_request_context

        self._remove_db_file()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self._remove_db_file()

    def _remove_db_file(self):
        try:
            os.remove(TEST_DATABASE_PATH)
        except OSError:
            pass

    def get(self, *args, **kwargs):
        # Override this to e.g. inject headers for all tests of a subclass
        return self.app.get(*args, **kwargs)


def seed_database(filename=TEST_DATABASE_PATH):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + filename

    from clubs import factories

    for _ in range(10):
        db.session.add(factories.ClubFactory())
        db.session.add(factories.I18NClubFactory())

    db.session.commit()
