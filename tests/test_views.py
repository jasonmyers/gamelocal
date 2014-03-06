# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from app import app
from flask import url_for


class TestViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.context = self.app.application.test_request_context

    def tearDown(self):
        pass

    def test_home(self):
        r = self.app.get('/')
        self.assertIn('Welcome to gamelocal!', r.data)

    def test_404(self):
        r = self.app.get('/notvalid')
        self.assertIn('Oops! Took a wrong turn somewhere...', r.data)
        with self.context('/notvalid'):
            self.assertIn(url_for('home'), r.data)


if __name__ == '__main__':
    unittest.main()
