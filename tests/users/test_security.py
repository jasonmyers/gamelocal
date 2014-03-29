# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import sys
import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from tests.utils import BaseTestCase


class TestCase(BaseTestCase):
    def test_has_control_characters(self):
        import string
        from app.users.security import has_control_characters as hcc

        # Allow these
        self.assertFalse(hcc(''))
        self.assertFalse(hcc('gamelocal'))
        self.assertFalse(hcc('game local'))
        self.assertFalse(hcc('プレーヤープレーヤー'))
        self.assertFalse(hcc(unicode(string.ascii_letters)))
        self.assertFalse(hcc(unicode(string.digits)))
        self.assertFalse(hcc(unicode(string.punctuation)))

        # U+0000 - U+001F
        for i in range(0x00, 0x1F + 1):
            self.assertTrue(hcc(unichr(i)))

        # U+007F - U+009F
        for i in range(0x7F, 0x9F + 1):
            self.assertTrue(hcc(unichr(i)))

        for ws in (s for s in unicode(string.whitespace) if s != ' '):
            self.assertTrue(hcc(ws))

        # Some other unicode control characters
        self.assertTrue(hcc('\uFFF9'))
        self.assertTrue(hcc('\uFFFA'))
        self.assertTrue(hcc('\uFFFB'))

        # These two are not strictly control characters, but they are invisible
        self.assertTrue(hcc('\u2028'))
        self.assertTrue(hcc('\u2029'))

        # Long word combination
        self.assertTrue(hcc('a' * 1023 + '\n'))

    def test_allow_password(self):
        from app.users.security import allow_password
        import string

        # Not long enough
        self.assertFalse(allow_password(''))
        self.assertFalse(allow_password('1234567'))

        # Just right
        self.assertTrue(allow_password('12345678'))
        self.assertTrue(allow_password('1' * 1024))

        # Too long
        self.assertFalse(allow_password('1' * 1025))

        # Special characters
        self.assertTrue(allow_password('プレーヤープレーヤー'))
        self.assertTrue(allow_password(unicode(
            string.ascii_letters + string.digits + string.punctuation + ' '
        )))

        # Control codes
        self.assertFalse(allow_password('12345678\t'))
        self.assertFalse(allow_password('1234\u20285678'))
        self.assertFalse(allow_password('\uFFF912345678'))


if __name__ == '__main__':
    unittest.main()
