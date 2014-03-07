# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app, db

TEST_DATABASE_PATH = os.path.join(basedir, 'test.db')


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + TEST_DATABASE_PATH

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(TEST_DATABASE_PATH)
        except OSError:
            pass

    def setUp(self):
        self.app = app.test_client()

        self.context = self.app.application.test_request_context

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get(self, *args, **kwargs):
        return self.app.get(*args, **kwargs)
