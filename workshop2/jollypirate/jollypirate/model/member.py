# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate import (
    exceptions,
    util
)
from jollypirate.model import BoatModel
from jollypirate.model.base import BaseModel
from jollypirate.util import types


class MemberModel(BaseModel):
    def __init__(self, first_name=None, last_name=None, ssn=None):
        super().__init__()

        self._name_first = None
        self._name_last = None
        self._social_sec_number = None
        self._boats = []

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
        return str(self.name_first + self.name_last) or ''

    @property
    def social_sec_number(self):
        return self._social_sec_number or 1337

    @social_sec_number.setter
    def social_sec_number(self, new_ssn):
        valid = _to_digits(new_ssn)
        if valid:
            self._social_sec_number = valid
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

    def remove_boat(self, boat_id):
        if any(boat.id == boat_id for boat in self.boats):
            self.log.info(
                'TODO: Remove boat "{!s}'.format(self.boats.get(boat_id))
            )

    def __hash__(self):
        return hash(
            (self.name_first, self.name_last, self.social_sec_number)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            (self.name_first, self.name_last, self.social_sec_number) ==
            (other.name_first, other.name_last, other.social_sec_number)
        )

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        _r = 'Member(first="{!s}", last="{!s}", ssn="{!s}", id="{!s}")'.format(
            self.name_first, self.name_last, self.social_sec_number, self.id
        )
        return _r

    @property
    def id(self):
        return abs(self.__hash__())


def _to_non_empty_string(input_):
    string = types.force_string(input_)
    if string.strip():
        return string
    return None


def _to_digits(input_):
    string = types.force_string(input_)
    if string:
        digits = util.text.extract_digits(string)
        if digits.strip():
            return digits
    return None
