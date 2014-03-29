# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from flask.ext.babel import lazy_gettext as _
from flask.ext.login import UserMixin, user_logged_in
from werkzeug.security import safe_str_cmp

from app import app, db
from app.models import BaseModel
from app.geo.models import Geo

from itsdangerous import BadData, TimedSerializer
from app.users.security import (auth_token_serializer,
    auth_token_serializer_perm)


class User(BaseModel, UserMixin, Geo):

    email = db.Column(db.UnicodeText, nullable=False, unique=True)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.UnicodeText, nullable=False, default='')
    locale = db.Column(db.UnicodeText, nullable=False, default='')

    last_login_date = db.Column(
        db.DateTime, nullable=False,
        default=db.func.now(),
    )

    def __unicode__(self):
        return self.email

    @property
    def nickname(self):
        """ Returns `name` if set, otherwise `email` """
        return self.name or self.email or ''

    def get_auth_token(self, serializer=None):
        """ Generates an auth token for this user

        By default this uses a serializer that will hold an expiration date

        :param serializer:
            A :mod:`itsdangerous` serializer with which to encode the token

            Defaults to `URLSafeTimedSerializer(app.secret_key)`

        Returns `None` if the user is lacking identification data

        Note:: logging in invalidates this token

        """
        if serializer is None:
            serializer = auth_token_serializer
        if self.id is None or self.last_login_date is None:
            return None
        return serializer.dumps(
            (unicode(self.id), self.last_login_date.isoformat())
        )

    def get_auth_token_perm(self):
        """ Generates an auth token for this user that does not expire

        Use with :meth:`from_auth_token_perm`

        """
        return self.get_auth_token(serializer=auth_token_serializer_perm)

    @classmethod
    def from_auth_token(cls, token, serializer=None, **kwargs):
        """ Given an auth token generated from :meth:`get_auth_token` return
        a :cls:`User` instance if the token is valid, or `None` if not

        :param token:
            An auth token generated from :meth:`get_auth_token`

        :param serializer:
            A :mod:`itsdangerous` serializer with which to decode the token

            Defaults to `URLSafeTimedSerializer(app.secret_key)`, and
            should be the same one that was used to generate the token

        :param kwargs:
            Additional kwargs to pass to the serializer, e.g. `max_age`

        """
        if serializer is None:
            serializer = auth_token_serializer

        if isinstance(serializer, TimedSerializer):
            if kwargs.get('max_age') is None:
                kwargs['max_age'] = app.config["REMEMBER_COOKIE_SECONDS"]

        try:
            user_id, user_last_login_date = serializer.loads(token, **kwargs)
        except (TypeError, ValueError):
            # Raised if fewer or more than 2 arguments were unpacked
            pass
        except BadData:
            # Raised if the token is expired or otherwise invalid
            pass
        else:
            user = cls.query.get(user_id)

            # Token is not valid if last_login_date has changed
            if user and safe_str_cmp(
                user.last_login_date.isoformat(), user_last_login_date
            ):
                return user

        return None

    @classmethod
    def from_auth_token_perm(cls, token):
        """ Recovers a user from a non-expiring auth token

        Use with :meth:`gen_auth_token_perm`

        """
        return cls.from_auth_token(
            token, serializer=auth_token_serializer_perm,
        )

    @classmethod
    def update_last_login_date(cls, app, user):
        new_login_date = datetime.datetime.utcnow()
        cls.query.filter_by(id=user.id).update({
            'last_login_date': new_login_date,
        })
        db.session.commit()


user_logged_in.connect(User.update_last_login_date)
