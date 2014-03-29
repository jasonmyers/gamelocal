# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os
import mock
import datetime

from werkzeug.security import generate_password_hash

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from tests.utils import BaseTestCase

from flask import url_for
from app import db


class TestViews(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        from app.users.models import User
        cls.User = User

        from tests.users.factories import ChessUserFactory, GoUserFactory
        cls.ChessUserFactory = ChessUserFactory
        cls.GoUserFactory = GoUserFactory

    def setUp(self):
        super(TestViews, self).setUp()
        self.ctx = self.context()
        self.ctx.push()

    def tearDown(self):
        super(TestViews, self).tearDown()
        self.ctx.pop()

    def test_register(self):
        data = self.get(url_for('users.register'))
        self.assertIn('Confirm Password', data)

    def test_register_submit(self):

        self.assertLength(self.User.query.all(), 0)

        user = self.ChessUserFactory()

        environ_base = {
            'HTTP_ACCEPT_LANGUAGE': '',
        }

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            },
            environ_base=environ_base,
        )

        self.assertIn('Welcome {}'.format(user.name), data)
        self.assertLength(self.User.query.all(), 1)

        created_user = self.User.query.first()
        self.assertEqual(created_user.name, user.name)
        self.assertNotEqual(created_user.password, user.password)
        self.assertIsNotNone(created_user.last_login_date)
        self.assertEqual(created_user.locale, '')

    def test_register_password_special_characters(self):
        import string
        user = self.ChessUserFactory(
            password=unicode(
                string.ascii_letters + string.digits +
                string.punctuation + ' ' + 'プレーヤープレーヤー'
            )
        )

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            }
        )

        self.assertIn('Welcome {}'.format(user.name), data)
        self.assertLength(self.User.query.all(), 1)

    @mock.patch('app.geo.models.iplookup')
    def test_register_submit_i18n(self, mock_iplookup):
        from tests.utils import gettext_for
        _ = gettext_for('ja')

        mock_iplookup.return_value = {
            'country_code': 'JP', 'city': 'Tokyo',
            'latitude': '35.6895', 'longitude': '139.6917',
        }

        self.assertLength(self.User.query.all(), 0)

        user = self.GoUserFactory()

        environ_base = {
            'HTTP_ACCEPT_LANGUAGE': 'ja',
            'REMOTE_ADDR': '127.0.0.1',
        }
        self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            },
            environ_base=environ_base,
        )

        self.assertLength(self.User.query.all(), 1)
        created_user = self.User.query.first()

        # Page should be localized from HTTP_ACCEPT_LANGUAGE header
        # and stored into user.locale
        self.assertIn('{} {}'.format(_('Welcome'), user.name),
                      self.get(url_for('home')))

        # Page unlocalized, not passing in header and user logged out
        self.get(url_for('users.logout'))
        self.assertIn('Login', self.get(url_for('home')))

        self.assertEqual(created_user.name, user.name)
        self.assertEqual(created_user.email, user.email)
        self.assertEqual(created_user.email_confirmed, False)
        self.assertNotEqual(created_user.password, user.password)
        self.assertIsNotNone(created_user.last_login_date)
        self.assertEqual(created_user.locale, 'ja')
        self.assertEqual(created_user.country_code, 'JP')
        self.assertEqual(created_user.city, 'Tokyo')
        self.assertEqual(created_user.latitude, 35.6895)
        self.assertEqual(created_user.longitude, 139.6917)

    def test_register_password_not_matched(self):
        user = self.ChessUserFactory()

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': '!' + user.plaintext_password,
            }
        )

        self.assertIn('Passwords must match', data)
        self.assertLength(self.User.query.all(), 0)

    def test_register_password_too_short(self):
        user = self.ChessUserFactory(password="1234567")

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            }
        )

        self.assertIn('Your password must contain', data)
        self.assertLength(self.User.query.all(), 0)

    def test_register_password_too_long(self):
        user = self.ChessUserFactory(password="a" * 2048)

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            }
        )

        self.assertIn('Your password must contain', data)
        self.assertLength(self.User.query.all(), 0)

    def test_register_password_control_character(self):
        user = self.ChessUserFactory(password="12345678\u0000")

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            },
        )

        self.assertIn('Your password must contain', data)
        self.assertLength(self.User.query.all(), 0)

    def test_register_email_taken(self):
        user = self.make_user()

        data = self.post(
            url_for('users.register'),
            data={
                'name': user.name,
                'email': user.email,
                'password': user.plaintext_password,
                'confirm': user.plaintext_password,
            },
        )

        self.assertIn('This email is already taken', data)

        self.assertLength(self.User.query.all(), 1)

    def test_register_required(self):
        data = self.post(
            url_for('users.register'),
            data={},
        )

        self.assertIn('required', data)

    def test_login(self):
        data = self.get(
            url_for('users.login'),
        )

        self.assertIn('Forgot Password', data)

    def test_login_required(self):
        data = self.post(
            url_for('users.login'),
            data={},
        )

        self.assertIn('Invalid email or password', data)

    def test_login_invalid_email(self):
        user = self.make_user()
        self.assertIsNone(
            self.User.query.filter_by(email='!' + user.email).first()
        )
        data = self.post(
            url_for('users.login'),
            data={
                'email': '!' + user.email,
                'password': user.plaintext_password,
            },
        )

        self.assertIn('Invalid email or password', data)

    def test_login_invalid_password(self):
        user = self.make_user()

        data = self.post(
            url_for('users.login'),
            data={
                'email': user.email,
                'password': '!' + user.plaintext_password,
            },
        )

        self.assertIn('Invalid email or password', data)

    def test_login_valid(self):
        user = self.make_user()

        data = self.post(
            url_for('users.login'),
            data={
                'email': user.email,
                'password': user.plaintext_password,
            },
        )

        self.assertIn('Welcome {}'.format(user.name), data)

    def test_login_next(self):
        user = self.make_user()

        data = self.get(
            url_for('users.login', next="/clubs/new")
        )
        self.assertIn('login?next=/clubs/new', data)

        data = self.post(
            url_for('users.login', next="/clubs/new"),
            data={
                'email': user.email,
                'password': user.plaintext_password,
            },
        )
        self.assertIn('Add Club', data)

    def test_last_login_date(self):
        user = self.make_user(last_login_date=datetime.datetime.min)
        initial = user.last_login_date

        self.post(
            url_for('users.login'),
            data={
                'email': user.email,
                'password': user.plaintext_password,
            },
        )
        after_login = user.last_login_date
        self.assertGreater(after_login, initial)

        self.get(url_for('home'))
        after_refresh = user.last_login_date
        self.assertEqual(after_refresh, after_login)

    def test_logout_logged_in(self):
        user = self.make_user()

        data = self.post(
            url_for('users.login'),
            data={
                'email': user.email,
                'password': user.plaintext_password,
            },
        )

        self.assertIn('Welcome {}'.format(user.name), data)

        data = self.get(url_for('users.logout'))

        self.assertIn('Login', data)

    def test_logout_logged_out(self):
        data = self.get(url_for('home'))
        self.assertIn('Login', data)

        data = self.get(url_for('users.logout'))
        self.assertIn('Login', data)

    def test_forgot_password_required(self):
        data = self.post(
            url_for('users.login'),
            data={
                'forgot_password': 'Forgot Password',
            },
        )

        self.assertIn('required', data)

    def test_forgot_password_invalid_email(self):
        user = self.make_user()

        data = self.post(
            url_for('users.login'),
            data={
                'forgot_password': 'Forgot Password',
                'email': '!' + user.email,
            },
        )

        # We show 'success' for invalid emails, to prevent fishing
        self.assertIn('An email has been sent', data)

    def test_forgot_password_valid(self):
        user = self.make_user()

        data = self.post(
            url_for('users.login'),
            data={
                'forgot_password': 'Forgot Password',
                'email': user.email,
            },
        )

        # We show 'success' for invalid emails, to prevent fishing
        self.assertIn('An email has been sent', data)

    @unittest.skip
    def test_forgot_password_email_sent(self):
        # TODO
        pass

    def test_reset_password_missing_token(self):
        data = self.get(url_for('users.reset_password'))

        self.assertIn('Bad token', data)
        self.assertIn('Forgot Password', data)

    def test_reset_password_invalid_token(self):
        data = self.get(url_for('users.reset_password', token="!"))

        self.assertIn('Bad token', data)
        self.assertIn('Forgot Password', data)

    def test_reset_password_valid_token(self):
        user = self.make_user()
        token = user.get_auth_token()
        data = self.get(url_for('users.reset_password', token=token))

        self.assertIn('New Password', data)

    def test_reset_password_submit_missing_token(self):
        data = self.post(
            url_for('users.reset_password'),
            data={
                'password': 'new_password',
                'confirm': 'new_password',
            }
        )

        self.assertIn('Bad token', data)
        self.assertIn('Forgot Password', data)

    def test_reset_password_submit_invalid_token(self):
        data = self.post(
            url_for('users.reset_password'),
            data={
                'password': 'new_password',
                'confirm': 'new_password',
                'token': '!',
            }
        )

        self.assertIn('Bad token', data)
        self.assertIn('Forgot Password', data)

    def test_reset_password_submit_valid_token(self):
        user = self.make_user()

        old_password = user.password

        token = user.get_auth_token()

        data = self.post(
            url_for('users.reset_password'),
            data={
                'password': 'new_password',
                'confirm': 'new_password',
                'token': token,
            }
        )

        self.assertIn('has been changed', data)
        self.assertIn('Welcome {}'.format(user.name), data)

        self.assertNotEqual(old_password, user.password)

    def test_reset_password_resubmit_valid_token(self):
        user = self.make_user()

        old_password = user.password

        token = user.get_auth_token()

        data = self.post(
            url_for('users.reset_password'),
            data={
                'password': 'new_password',
                'confirm': 'new_password',
                'token': token,
            }
        )

        self.assertIn('has been changed', data)
        self.assertIn('Welcome {}'.format(user.name), data)

        self.assertNotEqual(old_password, user.password)

        data = self.post(
            url_for('users.reset_password'),
            data={
                'password': 'new_password2',
                'confirm': 'new_password2',
                'token': token,
            }
        )

        self.assertIn('Bad token', data)

    def test_reset_password_expired_token(self):
        user = self.make_user()
        token = user.get_auth_token()

        with self.config(PASSWORD_RESET_SECONDS=-1):
            data = self.get(url_for('users.reset_password', token=token))

        self.assertIn('Bad token', data)

    def test_login_required(self):
        user = self.make_user()

        with self.enable_login():
            data = self.get(url_for('clubs.new_club'))

            self.assertIn('Password', data)

            data = self.post(
                url_for('users.login', next=url_for('clubs.new_club')),
                data={
                    'email': user.email,
                    'password': user.plaintext_password,
                }
            )

            self.assertIn('Add Club', data)


if __name__ == '__main__':
    unittest.main()
