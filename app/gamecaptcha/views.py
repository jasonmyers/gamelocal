# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, request, jsonify

from .forms.boards import GAMECAPTCHA_BOARDS

blueprint = Blueprint('gamecaptcha', __name__, url_prefix='/gamecaptcha')


@blueprint.route('/')
def get_gamecaptcha():

    data = request.get_json(silent=True) or request.args

    game = data.get('game')

    if game not in GAMECAPTCHA_BOARDS:
        return "game not specified", 404

    response = {
        'board_code': unicode(GAMECAPTCHA_BOARDS[game].generate_board()),
    }

    return jsonify(response)
