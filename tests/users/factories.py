# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
from werkzeug.security import generate_password_hash

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

import factory

from app.users.models import User

from tests.factories import BaseFactory
from tests.utils import gettext_for


def i18n_name(locale='en', fmt='{game}{n}'):
    def name(user, n):
        game = gettext_for(locale)(str(user.game))
        return fmt.format(
            game=game.decode('utf-8'),
            n=n,
        )
    return name


class UserFactory(BaseFactory):
    FACTORY_FOR = User
    FACTORY_HIDDEN_ARGS = ('game',)

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        # Hash the password for the test database, but store the plaintext
        # password on the user instance for testing
        plaintext_password = kwargs['password']
        kwargs['password'] = generate_password_hash(plaintext_password)
        instance = target_class(*args, **kwargs)
        instance.plaintext_password = plaintext_password
        return instance


class ChessUserFactory(UserFactory):
    FACTORY_FOR = User
    game = 'chess'

    name = factory.LazyAttributeSequence(
        i18n_name('en', "{game} User {n}")
    )
    email = factory.LazyAttributeSequence(
        i18n_name('en', "{game}.user+{n}@gamelocal.net")
    )
    password = 'gamelocal'


class GoUserFactory(UserFactory):
    FACTORY_FOR = User
    game = 'go'

    name = factory.LazyAttributeSequence(
        i18n_name('ja', "プレーヤー{game} {n}")
    )
    email = factory.LazyAttributeSequence(
        i18n_name('ja', "{game}.プレーヤー+{n}@gamelocal.net")
    )
    password = 'プレーヤープレーヤー'
