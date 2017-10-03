# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate import exceptions
from .. import util
from ..util import types


class MemberModel(object):
    def __init__(self, first_name=None, last_name=None, ssn=None):
        self._name_first = None
        self._name_last = None
        self._social_security_number = None

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
    def social_security_number(self):
        return self._social_security_number or 1337

    @social_security_number.setter
    def social_security_number(self, new_ssn):
        valid = _to_digits(new_ssn)
        if valid:
            self._social_security_number = valid
        else:
            raise exceptions.InvalidUserInput(
                'Expected social security number to contain at least one digit'
            )

    def __hash__(self):
        return hash(
            (self.name_first, self.name_last, self.social_security_number)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (
            (self.name_first, self.name_last, self.social_security_number) ==
            (other.name_first, other.name_last, other.social_security_number)
        )

    def __ne__(self, other):
        return not (self == other)

    @property
    def id(self):
        return self.__hash__()


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
