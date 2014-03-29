# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import mock
import json

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from tests.utils import BaseTestCase


TEST_IP = '66.249.68.74'
TEST_IP_RESPONSE = {'city': 'Mountain View'}


class TestLookup(BaseTestCase):

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_iplookup_valid(self, mock_urlopen):
        from app.geo.lookup import iplookup, GEO_IP_SERVICE

        mock_urlopen().read.return_value = json.dumps(TEST_IP_RESPONSE)

        self.assertEqual(iplookup(TEST_IP)['city'], TEST_IP_RESPONSE['city'])

        mock_urlopen.assert_called_with(GEO_IP_SERVICE.format(ip=TEST_IP))

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_iplookup_missing(self, mock_urlopen):
        from app.geo.lookup import iplookup

        self.assertEqual(iplookup(''), {})

        self.assertItemsEqual(mock_urlopen.call_args_list, [])

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_iplookup_invalid(self, mock_urlopen):
        from app.geo.lookup import iplookup, GEO_IP_SERVICE
        from urllib2 import HTTPError

        mock_urlopen().read.side_effect = HTTPError(
            '-1', 404, None, None, None)

        self.assertEqual(iplookup('-1'), {})

        mock_urlopen.assert_called_with(GEO_IP_SERVICE.format(ip='-1'))

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_iplookup_service_unavailable(self, mock_urlopen):
        from app.geo.lookup import iplookup, GEO_IP_SERVICE
        from urllib2 import HTTPError

        mock_urlopen().read.side_effect = HTTPError(
            '-1', 500, None, None, None)

        self.assertEqual(iplookup(TEST_IP), {})

        mock_urlopen.assert_called_with(GEO_IP_SERVICE.format(ip=TEST_IP))

    @mock.patch('app.geo.lookup.urllib2.urlopen')
    def test_iplookup_malformed(self, mock_urlopen):
        from app.geo.lookup import iplookup, GEO_IP_SERVICE

        mock_urlopen().read.return_value = """<!DOCTYPE html><html></html>"""

        self.assertEqual(iplookup(TEST_IP), {})

        mock_urlopen.assert_called_with(GEO_IP_SERVICE.format(ip=TEST_IP))


if __name__ == '__main__':
    unittest.main()
