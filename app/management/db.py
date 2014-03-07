# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import db


def reset():
    print "Dropping local database"

    db.drop_all()

    print "Creating new local database"

    db.create_all()

    print "Populating local database with initial data"
