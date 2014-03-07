# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory

from app.clubs.models import Club


class ClubFactory(factory.Factory):
    FACTORY_FOR = Club

    name = factory.Sequence(lambda n: "Go Club {}".format(n))


class I18NClubFactory(ClubFactory):
    name = factory.Sequence(lambda n: "楽しい囲碁クラブ {}".format(n))
