# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import db
from app.models import BaseModel


class Club(BaseModel):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(500))

    def __unicode__(self):
        return 'Club {}'.format(self.name)
