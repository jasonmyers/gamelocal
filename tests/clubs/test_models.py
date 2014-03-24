# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os

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
        from app.clubs.models import Club
        cls.Club = Club

    def setUp(self):
        super(TestModels, self).setUp()

        from factories import ChessClubFactory, GoClubFactory
        self.ChessClubFactory = ChessClubFactory
        self.GoClubFactory = GoClubFactory

    def test_club_model(self):
        club = self.ChessClubFactory()

        db.session.add(club)
        db.session.commit()

        self.assertIsNotNone(club.id)

        loaded = self.Club.query.get(club.id)
        self.assertEqual(loaded.name, club.name)

    def test_club_model_i18n(self):
        club = self.GoClubFactory()

        # Make sure we're dealing with a non-ascii name
        try:
            unicode.encode(club.name, 'ascii')
        except UnicodeEncodeError:
            pass
        else:
            raise self.failureException(
                "Expected non-ascii club name, got '{}'".format(club.name)
            )

        db.session.add(club)
        db.session.commit()

        self.assertIsNotNone(club.id)

        loaded = self.Club.query.get(club.id)
        self.assertEqual(loaded.name, club.name)

    def test_club_game_type_filter(self):
        db.session.add_all([self.GoClubFactory(), self.ChessClubFactory()])
        db.session.commit()

        self.assertLength(self.Club.query.all(), 2)
        self.assertLength(self.Club.query.filter_by(game='go').all(), 1)
        self.assertLength(self.Club.query.filter_by(game='chess').all(), 1)


if __name__ == '__main__':
    unittest.main()
