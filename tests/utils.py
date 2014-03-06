# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.context = self.app.application.test_request_context

    def tearDown(self):
        pass

    def get(self, *args, **kwargs):
        return self.app.get(*args, **kwargs)
