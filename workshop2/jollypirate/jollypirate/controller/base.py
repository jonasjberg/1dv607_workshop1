# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import string

from .. import exceptions
from ..model import member_registry
from ..view import MenuItem


# Dictionary keyed by integers storing lower-case characters.
INT_CHAR_LOOKUP = {k: v for k, v in enumerate(string.ascii_lowercase, 1)}


class BaseController(object):
    def __init__(self, model, view):
        self.log = logging.getLogger(str(self))

        self._model = None
        self._view = None

        self.model = model
        self.view = view

        self.member_registry = member_registry.singleton()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model):
        self._model = new_model

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, new_view):
        self._view = new_view

    def populate_model_data(self, model_, model_field, field_name,
                            should_choose_one_of=None):
        _valid = False
        while not _valid:
            _user_input = self.view.get_field_data(field_name,
                                                   should_choose_one_of)
            try:
                setattr(model_, model_field, _user_input)
            except (exceptions.InvalidUserInput,
                    exceptions.JollyPirateModelError) as e:
                self.view.display_msg_failure(e)
                if self.view.should_abort():
                    return
            else:
                _valid = True

    def _members_as_menu_items(self, members):
        out = {}
        for i, member in enumerate(members):
            _full_name = '{!s} {!s}'.format(member.name_first, member.name_last)
            _key = MenuItem(shortcut=self.int_to_char(i+1),
                            description=_full_name)
            out[_key] = member
        return out

    @staticmethod
    def int_to_char(number):
        _num_chars = len(INT_CHAR_LOOKUP)
        _default = min(max(0, _num_chars - number), _num_chars)
        assert _default >= 0
        return INT_CHAR_LOOKUP.get(number, INT_CHAR_LOOKUP.get(_default))
