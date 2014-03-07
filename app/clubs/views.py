# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template, Blueprint, request, url_for, redirect, flash
from flask.ext.babel import gettext as _

from app import db
from app.clubs.models import Club
from app.clubs.forms import ClubForm

blueprint = Blueprint('clubs', __name__, url_prefix='/clubs')


@blueprint.route('/')
def list_clubs():
    clubs = Club.query.all()
    return render_template('clubs/list.html', clubs=clubs)


@blueprint.route('/new', methods=['GET', 'POST'])
def new_club():
    form = ClubForm(request.form)

    if form.validate_on_submit():
        club = Club(
            name=form.name.data,
            game=form.game.data,
        )

        db.session.add(club)
        db.session.commit()
        flash(_('{club.name} has been added!'.format(club=club)))
        return redirect(url_for('.list_clubs'))

    return render_template('clubs/new.html', form=form)
