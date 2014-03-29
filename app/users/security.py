# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unicodedata import category
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer

from app import app

auth_token_serializer = URLSafeTimedSerializer(app.secret_key)
auth_token_serializer_perm = URLSafeSerializer(app.secret_key)


REJECT_CHARACTERS = ('\u2028', '\u2029')


def has_control_characters(s):
    """ Return True if the given string contains any unprintable/control
    characters
    """
    cat = category
    return any(
        cat(letter).startswith('C')  # Control character
        or letter in REJECT_CHARACTERS
        for letter in s
    )


def allow_password(password):
    """ Current password strength rules are::

        1) unicode allowed
        2) only "printable" characters (e.g. excluding control characters)
        3) at least 8 characters
        4) fewer than 1024 characters (arbitrarily large)

    """
    if not 8 <= len(password) <= 1024:
        return False

    if has_control_characters(password):
        return False

    return True
