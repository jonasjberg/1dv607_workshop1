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

        _valid_first_name = False
        while not _valid_first_name:
            _user_input = self.view.get_member_field('First Name')
            try:
                _new_member.name_first = _user_input
            except exceptions.InvalidUserInput as e:
                self.view.display_error(e)
                if self.view.should_abort():
                    return
            else:
                _valid_first_name = True

        _user_input = self.view.get_member_field('Last Name')
        try:
            _new_member.name_last = _user_input
        except exceptions.InvalidUserInput as e:
            self.view.display_error(e)

        # try:
        #     self.member_registry.add(member)
        # except exceptions.JollyPirateModelError as e:
        #     self.view.display_error(str(e))

    def update(self):
        # TODO: ..
        print('TODO: MemberController.update()')

    def list_all(self):
        _members = self.member_registry.getall()
        self.view.list(_members)

    def _filter(self, members):
        # TODO:  Return a subset of all members.
        return []







