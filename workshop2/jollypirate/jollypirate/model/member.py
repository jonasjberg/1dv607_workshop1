# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

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
        string = types.force_string(new_name)
        if string.strip():
            self._name_first = string
        else:
            raise ValueError('Expected first name to be a non-empty string')

    @property
    def name_last(self):
        return self._name_last or ''

    @name_last.setter
    def name_last(self, new_name):
        string = types.force_string(new_name)
        if string.strip():
            self._name_last = string
        else:
            raise ValueError('Expected last name to be a non-empty string')

    @property
    def social_security_number(self):
        return self._social_security_number or ''

    @social_security_number.setter
    def social_security_number(self, new_ssn):
        digits = util.text.extract_digits(new_ssn)
        if digits.strip():
            self._social_security_number = digits
        else:
            raise ValueError(
                'Expected social security number to contain digits'
            )

    def __hash__(self):
        return hash(
            (self.name_first, self.name_last, self.social_security_number)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return (
                (self.name_first, self.name_last, self.social_security_number) ==
                (other.name_first, other.name_last, other.social_security_number)
            )

    def __ne__(self, other):
        return not (self == other)

    @property
    def id(self):
        return self.__hash__()




