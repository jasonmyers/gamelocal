from wtforms.fields import Field

from . import widgets
from .validators import ChessCaptcha, GoCaptcha

__all__ = ["ChessCaptchaField", "GoCaptchaField"]


class ChessCaptchaField(Field):
    widget = widgets.ChessCaptchaWidget()

    captcha_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [ChessCaptcha()]
        super(ChessCaptchaField, self).__init__(label, validators, **kwargs)


class GoCaptchaField(Field):
    widget = widgets.GoCaptchaWidget()

    captcha_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [GoCaptcha()]
        super(GoCaptchaField, self).__init__(label, validators, **kwargs)
