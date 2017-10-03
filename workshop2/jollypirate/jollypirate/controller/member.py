# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate import exceptions
from jollypirate.model import MemberModel
from .base import BaseController


class MemberController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        # TODO: ..
        print('TODO: MemberController.delete()')

    def get_info(self):
        # TODO: ..
        print('TODO: MemberController.get_info()')

    def register(self):
        self.view.msg_member_registration_start()

        _new_member = MemberModel()

        self._populate_model_data(
            _new_member, model_field='name_first', field_name='First Name'
        )
        self._populate_model_data(
            _new_member, model_field='name_last', field_name='Last Name'
        )
        self._populate_model_data(
            _new_member, model_field='social_security_number',
            field_name='Social Security Number'
        )

        try:
            self.member_registry.add(_new_member)
        except exceptions.JollyPirateModelError as e:
            self.view.display_error(e)

    def update(self):
        # TODO: ..
        print('TODO: MemberController.update()')

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
                self.view.display_error(e)
                if self.view.should_abort():
                    return
            else:
                _valid = True







