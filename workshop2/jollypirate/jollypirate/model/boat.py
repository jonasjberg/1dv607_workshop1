# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se
from jollypirate import exceptions
from jollypirate.model.base import BaseModel
from jollypirate.util import types


class BoatType(object):
    KAYAK = 'KAYAK'
    MOTORSAILER = 'MOTORSAILER'
    OTHER = 'OTHER'
    SAILBOAT = 'SAILBOAT'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def validate(cls, _raw_value):
        return _raw_value in cls.__dict__.values()

    @classmethod
    def all(cls):
        return list(cls.__dict__)


class BoatModel(BaseModel):
    def __init__(self, type_, length):
        super().__init__()

        self._type = None
        self._length = None

        # TODO: ..

    @property
    def type_(self):
        # Names that shadow built-ins get a trailing '_' by convention.
        return self._type or BoatType.UNKNOWN

    @type_.setter
    def type_(self, new_type):
        # Names that shadow built-ins get a trailing '_' by convention.
        if BoatType.validate(new_type):
            self._type = new_type
        else:
            _all_boat_types = ', '.join(str(t) for t in BoatType.all())
            raise exceptions.JollyPirateModelError(
                'Expected boat type to be one of "{}"'.format(_all_boat_types)
            )

    @property
    def length(self):
        return self._length or 0

    @length.setter
    def length(self, new_length):
        _number = types.force_integer(new_length)
        if not _number or _number <= 0:
            raise exceptions.JollyPirateModelError(
                'Expected length to be a positive number'
            )

        self._length = _number
