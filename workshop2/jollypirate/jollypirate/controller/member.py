# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import string
from copy import deepcopy

from jollypirate import exceptions
from jollypirate.model import MemberModel
from jollypirate.view.base import MenuItem
from .base import BaseController


class MemberController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        self.view.msg_member_deletion_start()

        _members = self.member_registry.getall()
        _candidates = self._members_as_menu_items(_members)
        _should_delete = self.view.get_selection_from(_candidates)
        if _should_delete:
            try:
                self.member_registry.remove(_should_delete)
            except exceptions.JollyPirateModelError as e:
                self.view.display_msg_failure(str(e))
                self.view.msg_member_deletion_failure()
            else:
                self.view.msg_member_deletion_success()

    def get_info(self):
        # TODO: ..
        print('TODO: MemberController.get_info()')

    def register(self):
        self.view.msg_member_registration_start()

        _new_member = MemberModel()

        # Data validation is handled in the model.
        self._populate_model_data(
            _new_member, model_field='name_first', field_name='First Name'
        )
        self._populate_model_data(
            _new_member, model_field='name_last', field_name='Last Name'
        )
        self._populate_model_data(
            _new_member, model_field='social_sec_number',
            field_name='Social Security Number'
        )

        try:
            self.member_registry.add(_new_member)
        except exceptions.JollyPirateModelError as e:
            self.view.display_error(e)
            self.view.msg_member_registration_failure()
        else:
            self.view.msg_member_registration_success()

    def modify(self):
        self.view.msg_member_modify_start()

        _members = self.member_registry.getall()
        _candidates = self._members_as_menu_items(_members)
        _should_modify = self.view.get_selection_from(_candidates)
        if not _should_modify:
            self.view.msg_member_modify_failure()
            return

        _member = deepcopy(_should_modify)
        self._populate_model_data(
            _member, model_field='name_first', field_name='First Name'
        )
        self._populate_model_data(
            _member, model_field='name_last', field_name='Last Name'
        )
        self._populate_model_data(
            _member, model_field='social_sec_number',
            field_name='Social Security Number'
        )

        try:
            self.member_registry.remove(_should_modify)
            self.member_registry.add(_member)
        except exceptions.JollyPirateModelError as e:
            self.view.display_msg_failure(str(e))
            self.view.msg_member_modify_failure()
        else:
            self.view.msg_member_modify_success()

    def list_all(self):
        _members = self.member_registry.getall()
        self.view.list(_members)

    def _filter(self, members):
        # TODO:  Return a subset of all members.
        return []

    def _populate_model_data(self, model_, model_field, field_name):
        _valid = False
        while not _valid:
            _user_input = self.view.get_member_field(field_name)
            try:
                setattr(model_, model_field, _user_input)
            except exceptions.InvalidUserInput as e:
                self.view.display_msg_failure(e)
                if self.view.should_abort():
                    return
            else:
                _valid = True

    def _members_as_menu_items(self, members):
        out = {}
        for i, member in enumerate(members):
            _key = MenuItem(shortcut=int_to_char(i+1),
                            description=member.name_full)
            out[_key] = member
        return out


# Dictionary keyed by integers storing lower-case characters.
INT_CHAR_LOOKUP = {k: v for k, v in enumerate(string.ascii_lowercase, 1)}


def int_to_char(number):
    _num_chars = len(INT_CHAR_LOOKUP)
    _default = min(max(0, _num_chars - number), _num_chars)
    return INT_CHAR_LOOKUP.get(number, INT_CHAR_LOOKUP.get(_default))


