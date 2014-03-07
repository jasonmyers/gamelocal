# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from tests.utils import BaseTestCase

from app import db


class TestClubs(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestClubs, cls).setUpClass()
        from app.clubs.models import Club
        cls.Club = Club

    def setUp(self):
        super(TestClubs, self).setUp()

        from factories import ClubFactory, I18NClubFactory
        self.ClubFactory = ClubFactory
        self.I18NClubFactory = I18NClubFactory

    def test_club_model(self):
        club = self.ClubFactory()

        db.session.add(club)
        db.session.commit()

        self.assertIsNotNone(club.id)

        loaded = self.Club.query.get(club.id)
        self.assertEqual(loaded.name, club.name)

    def test_club_model_i18n(self):
        club = self.I18NClubFactory()

        db.session.add(club)
        db.session.commit()

        self.assertIsNotNone(club.id)

        loaded = self.Club.query.get(club.id)
        self.assertEqual(loaded.name, club.name)


if __name__ == '__main__':
    unittest.main()
