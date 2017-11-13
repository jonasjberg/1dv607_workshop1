# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import hashlib
import re

from .. import exceptions
from ..util import types
from .boat import BoatModel
from .base import BaseModel


# This regex barely manages to validate dates, included for brevity.
# Insert arbitrarily complex validation of "Lugn Algorithm"-derived SSNs here..
RE_VALID_SOCIAL_SECURITY_NUMBER = re.compile(
    r'(19|20)\d{2}([01])\d[0-3]\d\d{4}'
)


class MemberModel(BaseModel):
    def __init__(self, first_name=None, last_name=None, ssn=None):
        super().__init__()
        self._name_first = None
        self._name_last = None
        self._social_sec_number = None
        self._boats = []

        if first_name is not None:
            self.name_first = first_name
        if last_name is not None:
            self.name_last = last_name
        if ssn is not None:
            self.social_sec_number = ssn

    @property
    def name_first(self):
        return self._name_first or ''

    @name_first.setter
    def name_first(self, new_name):
        valid = _to_non_empty_string(new_name)
        if not valid:
            raise exceptions.InvalidUserInput(
                'Expected first name to be a non-empty string'
            )
        else:
            self._name_first = valid

    @property
    def name_last(self):
        return self._name_last or ''

    @name_last.setter
    def name_last(self, new_name):
        valid = _to_non_empty_string(new_name)
        if valid:
            self._name_last = valid
        else:
            raise exceptions.InvalidUserInput(
                'Expected last name to be a non-empty string'
            )

    @property
    def name_full(self):
        return '{!s} {!s}'.format(self.name_first, self.name_last) or ''

    @property
    def social_sec_number(self):
        return self._social_sec_number or 1337

    @social_sec_number.setter
    def social_sec_number(self, new_ssn):
        digits = _to_digits(new_ssn)
        if digits:
            if RE_VALID_SOCIAL_SECURITY_NUMBER.match(digits):
                self._social_sec_number = digits
            else:
                raise exceptions.InvalidUserInput(
                    'Invalid social security number. Expected "YYYYMMDD-XXXX"'
                )
        else:
            raise exceptions.InvalidUserInput(
                'Expected social security number to contain at least one digit'
            )

    def add_boat(self, new_boat):
        if not isinstance(new_boat, BoatModel):
            raise exceptions.JollyPirateModelError(
                'Expected an instance of "BoatModel"'
            )

        self._boats.append(new_boat)

    @property
    def boats(self):
        return self._boats or []

    def remove_boat(self, boat_to_remove):
        if boat_to_remove in self.boats:
            # self.log.debug(
            #     'Removing boat "{!r}'.format(boat_to_remove)
            # )
            self._boats = [b for b in self.boats if b != boat_to_remove]

    @classmethod
    def copy(cls, other):
        _copy = cls()
        _copy.name_first = other.name_first
        _copy.name_last = other.name_last
        _copy.social_sec_number = other.social_sec_number
        for b in other.boats:
            _copy.add_boat(b)
        return _copy

    def __hash__(self):
        # Used at run-time as dictionary keys, etc. Uses a different randomized
        # seed for each execution. From the Python 3 docs;
        #
        # > Hash randomisation is turned on by default in Python 3.
        # > This is a security feature:
        # > Hash randomization is intended to provide protection against a
        # > denial-of-service caused by carefully-chosen inputs that exploit
        # > the worst case performance of a dict construction
        #
        # This method should not be used for IDs that should be consistent
        # across program execution runs, serialization, etc.
        return hash(
            (self.name_first, self.name_last, self.social_sec_number)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            (self.name_first, self.name_last, self.social_sec_number,
             self.boats, self.id) ==
            (other.name_first, other.name_last, other.social_sec_number,
             other.boats, other.id)
        )

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return (
            'Member(first="{!s}", last="{!s}", boats="{!s}", ssn="{!s}", '
            'id="{!s}")'.format(self.name_first, self.name_last, self.boats,
                                self.social_sec_number, self.id)
        )

    @property
    def id(self):
        # Consistent, unique ID for serialization and UI "handle".
        h = hashlib.md5()
        h.update(self.name_first.encode('utf-8'))
        h.update(self.name_last.encode('utf-8'))
        h.update(self.social_sec_number.encode('utf-8'))
        return abs(int(h.hexdigest(), 16))


def _to_non_empty_string(input_):
    string = types.force_string(input_)
    if string.strip():
        return string
    return None


def _to_digits(input_):
    string = types.force_string(input_)
    if string:
        digits = ''
        for char in string:
            if char.isdigit():
                digits += char

        if digits.strip():
            return digits

    return None
