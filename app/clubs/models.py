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

    name = db.Column(db.Unicode(500), nullable=False, default='')
    game = db.Column(
        UnicodeChoices(50, choices=CLUB_GAME_CHOICES),
        nullable=False
    )

    __mapper_args__ = {'polymorphic_on': game}

    def __unicode__(self):
        return 'Club {}'.format(self.name)


class GoClub(Club):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'go'}


class ChessClub(Club):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'chess'}
