# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from ..util import types


class MemberModel(object):
    def __init__(self, uuid):
        self.uuid = uuid

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




