# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

import mock
import json

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

        from app.clubs.models import GoClub
        self.GoClub = GoClub

        from tests.clubs.factories import GoClubFactory
        self.GoClubFactory = GoClubFactory

    def test_coords(self):
        club = self.GoClubFactory()

        self.assertEqual(club.coords, (30.0, 30.0))

    def test_querybounding_box(self):
        clubs = [self.GoClubFactory() for _ in range(5)]

        self.assertEqual(clubs[0].coords, (30.0, 30.0))
        self.assertEqual(clubs[-1].coords, (34.0, 34.0))

        db.session.add_all(clubs)
        db.session.commit()

        self.assertLength(
            self.GoClub.query_bounding_box(
                (30.0, 30.0),
                (34.0, 34.0),
            ).all(), 5
        )

        self.assertLength(
            self.GoClub.query_bounding_box(
                (31.0, 31.0),
                (33.0, 33.0),
            ).all(), 3
        )

        self.assertLength(
            self.GoClub.query_bounding_box(
                (28.0, 28.0),
                (29.0, 29.0),
            ).all(), 0
        )

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_set_geo_from_ip(self, mock_urlopen):
        TEST_IP = '66.249.68.74'
        TEST_IP_RESPONSE = {'city': 'Mountain View'}

        mock_urlopen().read.return_value = json.dumps(TEST_IP_RESPONSE)

        club = self.GoClubFactory()
        club.set_geo_from_ip(TEST_IP)

        self.assertEqual(club.city, TEST_IP_RESPONSE['city'])

    def test_set_geo_from_geo(self):
        geo1 = self.GoClubFactory()
        geo2 = self.GoClubFactory()

        self.assertNotEqual(geo1.latitude, geo2.latitude)

        geo2.set_geo_from_geo(geo1)

        self.assertEqual(geo1.latitude, geo2.latitude)


if __name__ == '__main__':
    unittest.main()
