# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (render_template, Blueprint, request, url_for, redirect,
                   flash, jsonify)
from flask.ext.babel import gettext as _
from flask.ext.login import login_required

from app import app, db
from app.clubs.models import Club
from app.clubs.forms import ClubForm

blueprint = Blueprint('clubs', __name__, url_prefix='/clubs')


@blueprint.route('/<club_id>')
def show_club(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('clubs/show.html', club=club)


@blueprint.route('/')
def list_clubs():
    clubs = Club.query.all()
    return render_template('clubs/list.html', clubs=clubs)


@blueprint.route('/new', methods=['GET', 'POST'])
@login_required
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


@blueprint.route('/map')
def map_clubs():
    southwest_arg = request.args.get('southwest')
    northeast_arg = request.args.get('northeast')

    try:
        southwest = tuple(float(pos) for pos in southwest_arg.split(','))
        northeast = tuple(float(pos) for pos in northeast_arg.split(','))
        if len(southwest) != 2 or len(northeast) != 2:
            raise ValueError
    except ValueError:
        return 'Invalid or missing boundary coordinates', 400

    clubs = Club.query_bounding_box(southwest, northeast).all()

    app.logger.debug(
        'Found {} clubs inside ({:.2f}, {:.2f}), ({:.2f}, {:.2f})'.format(
            len(clubs), southwest[0], southwest[1],
            northeast[0], northeast[1]
        )
    )

    return jsonify(clubs=[
        club.jsonify(
            url=url_for('clubs.show_club', club_id=club.id)
        )
        for club in clubs
    ])
