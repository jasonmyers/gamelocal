# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from contextlib import contextmanager

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from babel.support import Translations

from app import app, db
from tests import factories

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
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + TEST_DATABASE_PATH

        # Disable login_required for tests
        # Use self.enable_login() context manager to enable for a test
        app.login_manager._login_disabled = True

        # Disable session protection, since `follow_redirects=True` doesn't
        # seem to maintain request metadata (e.g. when using 'REMOTE_ADDR')
        # (Is there a better way?)
        app.login_manager.session_protection = None

    def setUp(self):
        self.app = app.test_client()

        self.context = self.app.application.test_request_context

        assert unicode(db.engine.url).startswith('sqlite:///')
        self._remove_db_file()
        db.create_all()

        factories.reset_all_sequences()

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
        """ Override this to e.g. inject headers for all tests of a subclass

        :param as_text:
            If True (default), returns just the text response.
            If False, returns the Response object
        """
        as_text = kwargs.pop('as_text', True)
        kwargs['follow_redirects'] = kwargs.get('follow_redirects', True)
        response = self.app.get(*args, **kwargs)
        if as_text:
            return response.get_data(as_text=True)
        return response

    def post(self, *args, **kwargs):
        """ Override this to e.g. inject headers for all tests of a subclass

        :param as_text:
            If True (default), returns just the text response.
            If False, returns the Response object
        """
        as_text = kwargs.pop('as_text', True)
        kwargs['follow_redirects'] = kwargs.get('follow_redirects', True)
        response = self.app.post(*args, **kwargs)
        if as_text:
            return response.get_data(as_text=True)
        return response

    @contextmanager
    def config(self, **kwargs):
        """ A context manager to temporarly alter the application config

        Usage::

            with self.config(CSRF_ENABLED=True):
                ...

        """
        backup_config = app.config.copy()
        app.config.update(kwargs)
        try:
            yield
        finally:
            app.config = backup_config

    @contextmanager
    def enable_login(self):
        app.login_manager._login_disabled = False
        try:
            yield
        finally:
            app.login_manager._login_disabled = True

    def make_user(self, *args, **kwargs):
        from tests.users.factories import ChessUserFactory
        kwargs['email'] = kwargs.get('email', 'valid@gamelocal.net')
        kwargs['password'] = kwargs.get('password', 'gamelocal')
        user = ChessUserFactory(
            *args, **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user


def gettext_for(locale='en'):
    """ Returns the `ugettext` function for a specific locale

    Usage::

        _ = gettext_for('ja')  # Load the 'ja' translation library

    """
    return Translations.load(
        os.path.join(BASEDIR, 'app', 'translations'), [locale]
    ).ugettext


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
