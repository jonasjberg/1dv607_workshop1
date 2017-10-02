# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .base import BaseController


class MemberController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        print('TODO: MemberController.delete()')

    def get_info(self):
        print('TODO: MemberController.get_info()')

    def register(self):
        print('TODO: MemberController.register()')

    def update(self):
        print('TODO: MemberController.update()')

    def list_all(self):
        _members = self.member_registry.getall()
        self.view.list(_members)

    def _filter(self, members):
        # TODO:  Return a subset of all members.
        return []
