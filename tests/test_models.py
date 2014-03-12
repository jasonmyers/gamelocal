# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os
from sqlalchemy.exc import StatementError

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from tests.utils import BaseTestCase

from app import db


class TestModels(BaseTestCase):

    def test_unicode_choices(self):
        from app.models import UnicodeChoices, InvalidChoiceError

        choices = [
            ('chess', 'Chess'), ('go', 'Go')
        ]

        field = UnicodeChoices(10, choices=choices)

        self.assertRaises(
            InvalidChoiceError, field.process_bind_param, 'parcheesi', None
        )

    def test_unicode_choices_model_commit(self):
        from tests.clubs.factories import GoClubFactory
        from app.clubs.models import Club, CLUB_GAME_CHOICES

        club = GoClubFactory()
        club.game = 'parcheesi'

        self.assertLength(Club.query.all(), 0)

        db.session.add(club)
        try:
            db.session.commit()
        except StatementError as e:
            self.assertIn('Invalid choice', e.message)
            db.session.rollback()
            self.assertLength(Club.query.all(), 0)
        else:
            raise self.failureException

    def test_unicode_choices_for(self):
        from tests.clubs.factories import GoClubFactory
        from app.clubs.models import CLUB_GAME_CHOICES

        club = GoClubFactory()

        self.assertEqual(
            club.choices_for('game'),
            dict(CLUB_GAME_CHOICES)
        )

        self.assertRaises(AttributeError, club.choices_for, 'name')

    def test_unicode_label_for_choice(self):
        from tests.clubs.factories import GoClubFactory
        from app.clubs.models import CLUB_GAME_CHOICES

        club = GoClubFactory()

        self.assertEqual(
            club.label_for_choice('game', 'go'),
            dict(CLUB_GAME_CHOICES)['go']
        )

        self.assertRaises(
            KeyError,
            club.label_for_choice, 'game', 'parcheesi'
        )

        self.assertRaises(
            AttributeError,
            club.label_for_choice, 'name', 'go',
        )


if __name__ == '__main__':
    unittest.main()
