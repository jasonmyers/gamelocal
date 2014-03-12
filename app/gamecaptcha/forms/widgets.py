# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Markup
from flask.json import JSONEncoder, dumps


try:
    from speaklater import _LazyString

    class _JSONEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, _LazyString):
                return str(o)
            return JSONEncoder.default(self, o)
except:
    _JSONEncoder = JSONEncoder


GAMECAPTCHA_HTML = '''
<script type="text/javascript">var gameCaptchaOptions = {options};</script>
<div id="gameCaptcha">
    <p></p>
    <div id="gameCaptchaButtons">
        <button type="button" id="gameCaptchaRefresh">Refresh</button>
    </div>
    <div id="gameCaptchaError"></div>
    <div id="gameCaptchaBoardContainer"></div>
    <input id="gameCaptchaChallenge"" type="hidden"
        name="gameCaptchaChallenge" value="" />
    <input id="gameCaptchaResponse" type="hidden"
        name="gameCaptchaResponse" />
    <input id="gameCaptchaGame" type="hidden"
        name="gameCaptchaGame" value="{game}" />
</div>
'''

__all__ = ["GameCaptchaWidget", "ChessCaptchaWidget", "GoCaptchaWidget"]

from boards import GAMECAPTCHA_BOARDS


class GameCaptchaWidget(object):

    instructions = ""

    def __init__(self, game):
        self.game = game

    def recaptcha_html(self, options):
        raise NotImplementedError

    def __call__(self, field, error=None, **kwargs):
        _ = field.gettext

        options = {
            'custom_translations': {
                'instructions': _(self.instructions),
                'incorrect_try_again': _('Incorrect. Try again.'),
                'load_error': _('There was a problem loading the captcha, '
                                'try refreshing the page.')
            }
        }

        return self.gamecaptcha_html(options)

    def gamecaptcha_html(self, options):
        html = GAMECAPTCHA_HTML

        return Markup(html.format(
            game=self.game,
            board_code=GAMECAPTCHA_BOARDS[self.game].generate_board(),
            options=dumps(options, cls=_JSONEncoder),
        ))


class ChessCaptchaWidget(GameCaptchaWidget):

    instructions = "Put the white king in check."

    def __init__(self):
        super(ChessCaptchaWidget, self).__init__(game='chess')


class GoCaptchaWidget(GameCaptchaWidget):

    instructions = "Capture the white group."

    def __init__(self):
        super(GoCaptchaWidget, self).__init__(game='go')
