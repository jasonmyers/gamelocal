# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

import factory


class BaseFactory(factory.Factory):
    pass


def reset_all_sequences():
    for Subclass in BaseFactory.__subclasses__():
        Subclass.reset_sequence()
