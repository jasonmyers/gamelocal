# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

import factory

from app.clubs.models import Club

from tests.utils import gettext_for


def i18n_name(locale='en', fmt='{game}{n}'):
    def name(club, n):
        game = gettext_for(locale)(Club.label_for_choice('game', club.game))
        return fmt.format(
            game=game.decode('utf-8'),
            n=n,
        )
    return name


class ChessClubFactory(factory.Factory):
    FACTORY_FOR = Club
    name = factory.LazyAttributeSequence(
        i18n_name('en', "{game} Club {n}")
    )
    game = 'chess'


class GoClubFactory(factory.Factory):
    FACTORY_FOR = Club
    name = factory.LazyAttributeSequence(
        i18n_name('ja', "楽しいクラブ{game} {n}")
    )
    game = 'go'
