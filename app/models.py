# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)
