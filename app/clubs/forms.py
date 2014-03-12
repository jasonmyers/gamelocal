# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import Required

from app.clubs.models import Club
from app.gamecaptcha.forms import GoCaptchaField, ChessCaptchaField


class ClubForm(Form):

    name = TextField(_('Club Name'), [Required()])
    game = SelectField(
        _('Game'), [Required()], choices=Club.choices_for('game').items(),
    )

    game_captcha = ChessCaptchaField()
