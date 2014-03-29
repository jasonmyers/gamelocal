# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import Required, Email, EqualTo


class LoginForm(Form):

    email = TextField(_('Email'), [Required(), Email()])
    password = PasswordField(_('Password'), [Required()])


class RegisterForm(Form):
    name = TextField(_('Name'))
    email = TextField(_('Email'), [Required(), Email()])
    password = PasswordField(_('Password'), [Required()])
    confirm = PasswordField(_('Confirm Password'), [
        Required(),
        EqualTo('password', message=_('Passwords must match'))
    ])

    recaptcha = RecaptchaField()


class ResetPasswordForm(Form):
    token = HiddenField()
    password = PasswordField(_('New Password'), [Required()])
    confirm = PasswordField(_('Confirm Password'), [
        Required(),
        EqualTo('password', message=_('Passwords must match'))
    ])

    recaptcha = RecaptchaField()
