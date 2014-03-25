# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import class_mapper

from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    create_date = db.Column(
        db.DateTime, nullable=False,
        default=db.func.now(),
    )

    update_date = db.Column(
        db.DateTime, nullable=False,
        default=db.func.now(), onupdate=db.func.now()
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    @classmethod
    def choices_for(cls, column):
        return class_mapper(cls).columns[column].type.choices

    @classmethod
    def label_for_choice(cls, column, choice):
        return unicode(cls.choices_for(column)[choice])


class InvalidChoiceError(Exception):
    pass


class UnicodeTextChoices(db.TypeDecorator):
    """A Unicode field that is restricted to a set of choices

    `choices`
        An iterable of tuples in the form (value, label)

    Usage::

        FRUIT_CHOICES = (('apple', 'Apple'), ('key_lime', 'Key Lime'))
        fruit = db.Column(db.UnicodeTextChoices(choices=FRUIT_CHOICES))

    """
    impl = db.UnicodeText

    EMPTY_CHOICE = (('', ''),)

    def __init__(self, choices=None, *args, **kwargs):
        if choices is None:
            choices = ()
        self.choices = OrderedDict(choices)
        super(UnicodeTextChoices, self).__init__(*args, **kwargs)

    def __repr__(self):
        return 'UnicodeTextChoices'

    def process_bind_param(self, value, dialect):
        if value not in self.choices:
            raise InvalidChoiceError('Invalid choice {}'.format(value))
        return value

    def process_result_value(self, value, dialect):
        return value
