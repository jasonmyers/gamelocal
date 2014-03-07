# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, SelectField
from wtforms.validators import Required

from app.clubs.models import Club


class ClubForm(Form):

    name = TextField(_('Club Name'), [Required()])
    game = SelectField(
        _('Game'), [Required()], choices=Club.choices_for('game').items(),
    )

    recaptcha = RecaptchaField()
