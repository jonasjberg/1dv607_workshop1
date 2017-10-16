# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .base import BaseModel
from .. import exceptions
from ..util import types


class BoatType(object):
    """
    Simple "struct"-like singleton class that wraps "constant" values and
    utility methods for accessing and formatting these "constants".
    """
    KAYAK = 'KAYAK'
    MOTORSAILER = 'MOTORSAILER'
    OTHER = 'OTHER'
    SAILBOAT = 'SAILBOAT'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def _boat_types(cls):
        return list(t for t in cls.__dict__.values()
                    if t and isinstance(t, str) and t.isupper())

    @classmethod
    def validate(cls, _raw_value):
        return (_raw_value and isinstance(_raw_value, str)
                and _raw_value.upper() in cls._boat_types())

    @classmethod
    def all(cls):
        return cls._boat_types()


class BoatModel(BaseModel):
    BOAT_TYPES = BoatType

    def __init__(self):
        super().__init__()

        self._type = None
        self._length = None

    @property
    def type_(self):
        # Names that shadow built-ins get a trailing '_' by convention.
        return self._type or self.BOAT_TYPES.UNKNOWN

    @type_.setter
    def type_(self, new_type):
        # Names that shadow built-ins get a trailing '_' by convention.
        if self.BOAT_TYPES.validate(new_type):
            self._type = new_type
        else:
            _all_boat_types = ', '.join(str(t) for t in self.BOAT_TYPES.all())
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

    def __hash__(self):
        return hash((self.type_, self.length))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            (self.type_, self.length) == (other.type_, other.length)
        )

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        _r = 'Boat(type="{!s}", length="{!s}")'.format(self.type_, self.length)
        return _r

    @property
    def id(self):
        return abs(self.__hash__())
