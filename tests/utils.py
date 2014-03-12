# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from babel.support import Translations

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

        assert unicode(db.engine.url).startswith('sqlite:///')
        self._remove_db_file()
        db.create_all()

    def tearDown(self):
        assert unicode(db.engine.url).startswith('sqlite:///')
        db.session.remove()
        db.drop_all()
        self._remove_db_file()

    def _remove_db_file(self):
        try:
            os.remove(TEST_DATABASE_PATH)
        except OSError:
            pass

    def assertLength(self, collection, length):
        self.assertEqual(len(collection), length)

    def get(self, *args, **kwargs):
        # Override this to e.g. inject headers for all tests of a subclass
        return self.app.get(*args, **kwargs)


def gettext_for(locale='en'):
    """ Returns the `gettext` function for a specific locale """
    return Translations.load(
        os.path.join(BASEDIR, 'app', 'translations'), [locale]
    ).gettext


def seed_database(filename=TEST_DATABASE_PATH):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + filename

    from clubs import factories

    for _ in range(2):
        for Factory in [
            factories.GoClubFactory,
            factories.ChessClubFactory,
        ]:
            db.session.add(Factory())

    db.session.commit()
