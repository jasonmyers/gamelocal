# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, Blueprint

from app.clubs.models import Club

blueprint = Blueprint('clubs', __name__, url_prefix='/clubs')


@blueprint.route('/')
def list_clubs():
    clubs = Club.query.all()
    return render_template('clubs/list.html', clubs=clubs)
