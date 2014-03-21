# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babel import lazy_gettext as _

from app import db
from app.models import BaseModel, UnicodeChoices


CLUB_GAME_CHOICES = (
    ('go', _('Go')),
    ('chess', _('Chess')),
)


class Club(BaseModel):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(500))

    game = db.Column(UnicodeChoices(50, choices=CLUB_GAME_CHOICES))

    def __unicode__(self):
        return 'Club {}'.format(self.name)
