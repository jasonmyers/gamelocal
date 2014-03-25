# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from tests.utils import BaseTestCase

from flask import url_for


class TestViews(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        from app.clubs.models import GoClub
        cls.GoClub = GoClub

    def setUp(self):
        super(TestViews, self).setUp()
        self.ctx = self.context()
        self.ctx.push()

    def tearDown(self):
        super(TestViews, self).tearDown()
        self.ctx.pop()

    def test_new_club(self):
        data = self.get(url_for('clubs.new_club'))
        self.assertIn('Name', data)

    def test_create_club_required(self):

        self.assertLength(self.GoClub.query.all(), 0)
        data = self.post(
            url_for('clubs.new_club'),
            data={}
        )

        self.assertIn('required', data)
        self.assertLength(self.GoClub.query.all(), 0)

    def test_create_club(self):
        self.assertLength(self.GoClub.query.all(), 0)

        self.post(
            url_for('clubs.new_club'),
            data={
                'name': 'test club',
                'game': 'go',
            }
        )

        clubs = self.GoClub.query.all()

        self.assertLength(clubs, 1)
        self.assertEqual(clubs[0].name, 'test club')


if __name__ == '__main__':
    unittest.main()
