# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from tests.utils import BaseTestCase

from flask import url_for


class TestViews(BaseTestCase):

    def setUp(self):
        super(TestViews, self).setUp()
        self.ctx = self.context()
        self.ctx.push()

    def tearDown(self):
        super(TestViews, self).tearDown()
        self.ctx.pop()

    def test_home(self):
        data = self.get(url_for('home'))
        self.assertIn('Welcome to GameLocal!', data)

    def test_404(self):
        data = self.get('/notvalid')
        self.assertIn('Oops! Took a wrong turn somewhere...', data)
        self.assertIn(url_for('home'), data)


if __name__ == '__main__':
    unittest.main()
