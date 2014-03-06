# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from tests.utils import BaseTestCase

from flask import url_for


class TestViews(BaseTestCase):

    def test_home(self):
        resp = self.get('/')
        data = resp.data.decode('utf-8')
        self.assertIn('Welcome to GameLocal!', data)

    def test_404(self):
        resp = self.get('/notvalid')
        data = resp.data.decode('utf-8')
        self.assertIn('Oops! Took a wrong turn somewhere...', data)
        with self.context('/notvalid'):
            self.assertIn(url_for('home'), data)


if __name__ == '__main__':
    unittest.main()
