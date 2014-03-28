# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.geo.lookup import iplookup
from app.models import UnicodeTextChoices
from app.geo.locale import COUNTRY_CODES, COUNTRY_CODES_DICT


class Geo(object):
    """ Geo Mixin to add address and location data to models """

    # free-form address lines
    address = db.Column(db.UnicodeText, nullable=False, default='')

    city = db.Column(db.UnicodeText, nullable=False, default='')

    # state / district / province
    region = db.Column(db.UnicodeText, nullable=False, default='')

    # zip
    postal_code = db.Column(db.UnicodeText, nullable=False, default='')

    # 2-digit ISO 3166-1 Alpha2 country code
    country_code = db.Column(
        UnicodeTextChoices(
            choices=UnicodeTextChoices.EMPTY_CHOICE + COUNTRY_CODES
        ),
        nullable=False, default=''
    )

    timezone = db.Column(db.UnicodeText, nullable=False, default='')

    @declared_attr
    def latitude(self):
        if db.engine.dialect.name == 'sqlite':
            return db.Column(db.Float)
        return db.Column(db.Numeric(precision=9, scale=6))

    @declared_attr
    def longitude(self):
        if db.engine.dialect.name == 'sqlite':
            return db.Column(db.Float)
        return db.Column(db.Numeric(precision=9, scale=6))

    GEO_ATTRS = (
        'address', 'city', 'region', 'postal_code', 'country_code',
        'timezone', 'latitude', 'longitude',
    )

    @property
    def country(self):
        """ Human readable version of country_code """
        return COUNTRY_CODES_DICT.get(self.country_code, self.country_code)

    @classmethod
    def query_bounding_box(cls, topleft, bottomright):
        """ Returns a query of Geo instances with lat/long inside
        the given bounding box

        :param topleft:
            tuple of coordinates specifying the top left
            position of the bounding box

        :param bottomright:
            tuple of coordinates specifying the bottom left
            position of the bounding box

        """
        return db.session.query(cls).filter(
            cls.latitude.between(topleft[0], bottomright[0]),
            cls.longitude.between(topleft[1], bottomright[1]),
        )

    @property
    def coords(self):
        return self.latitude, self.longitude

    def set_geo_from_ip(self, ip):
        """ Sets this model's geo data to the same as the given ip address

        If `force` is True, this will overrite existing data

        Usage ::

            user.set_geo_from_ip(user_ip)

        """
        geo_data = iplookup(ip)
        self.address = ''
        self.city = geo_data.get('city', '')
        self.region = geo_data.get('region_name', '')
        self.postal_code = geo_data.get('postal_code', '')

        country_code = geo_data.get('country_code', '')
        if country_code and country_code not in COUNTRY_CODES_DICT:
            country_code = ''
        self.country_code = country_code

        try:
            self.latitude = float(geo_data.get('latitude')) or None
        except (TypeError, ValueError):
            self.latitude = None

        try:
            self.longitude = float(geo_data.get('longitude')) or None
        except (TypeError, ValueError):
            self.longitude = None

        # The service returns 0, 0 for some invalid addresses, so we'll
        # treat those as None
        if (self.latitude, self.longitude) == (0.0, 0.0):
            self.latitude, self.longitude = None, None

    def set_geo_from_geo(self, other):
        """ Sets this model's geo data to the same as another geo model

        Usage ::

            club.set_geo_from_geo(user)

        """
        for attr in Geo.GEO_ATTRS:
            setattr(self, attr, getattr(other, attr))
