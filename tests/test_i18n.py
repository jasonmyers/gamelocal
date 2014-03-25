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


class TestViews_ja(BaseTestCase):
    """ Test i18n settings for 'ja' locale """

    def get(self, *args, **kwargs):
        # Force HTTP_ACCEPT_LANGUAGE header to be 'ja'
        environ_base = kwargs.get('environ_base', {})
        environ_base['HTTP_ACCEPT_LANGUAGE'] = 'ja'
        kwargs['environ_base'] = environ_base
        return super(TestViews_ja, self).get(*args, **kwargs)

    def test_home_ja(self):
        data = self.get('/')
        self.assertIn('地元のゲームへようこそ！', data)

    def test_404(self):
        data = self.get('/notvalid')
        self.assertIn('おっと！行方不明のページ！', data)
        with self.context('/notvalid'):
            self.assertIn('ホメパゲ', data)
            self.assertIn(url_for('home'), data)


if __name__ == '__main__':
    unittest.main()
