# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import datetime

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

import unittest

from tests.utils import BaseTestCase

from app import db


class TestModels(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestModels, cls).setUpClass()
        from app.users.models import User
        cls.User = User

    def setUp(self):
        super(TestModels, self).setUp()

        from tests.users.factories import ChessUserFactory, GoUserFactory
        self.ChessUserFactory = ChessUserFactory
        self.GoUserFactory = GoUserFactory

    def test_user_model(self):
        user = self.ChessUserFactory()

        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)

        loaded = self.User.query.get(user.id)
        self.assertEqual(loaded.name, user.name)
        self.assertEqual(unicode(loaded), loaded.email)

    def test_auth_token_missing_data(self):
        user = self.ChessUserFactory()

        self.assertEqual(user.get_auth_token(), None)

    def test_auth_token_valid(self):
        user = self.make_user()
        token = user.get_auth_token()

        self.assertIsNotNone(token)
        self.assertEqual(user, self.User.from_auth_token(token))

    def test_auth_token_invalid(self):
        user = self.make_user()
        token = user.get_auth_token()

        self.assertIsNone(self.User.from_auth_token('!' + token))

    def test_auth_token_arguments(self):
        from app.users.models import auth_token_serializer
        user = self.make_user()
        token = auth_token_serializer.dumps(
            (unicode(user.id), user.last_login_date.isoformat(), False)
        )
        self.assertIsNone(self.User.from_auth_token(token))

    def test_auth_token_force_expired(self):
        from app.users.models import auth_token_serializer
        user = self.make_user()
        token = user.get_auth_token()

        user.last_login_date = user.last_login_date + \
            datetime.timedelta(seconds=1)

        self.assertIsNone(self.User.from_auth_token(token))


if __name__ == '__main__':
    unittest.main()
