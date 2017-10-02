# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class MemberController(object):
    def __init__(self, view):
        self.view = view
        self._members = ['member_foo', 'member_bar']

    @classmethod
    def delete(cls):
        print('TODO: MemberController.delete()')

    @classmethod
    def get_info(cls):
        print('TODO: MemberController.get_info()')

    @classmethod
    def register(cls):
        print('TODO: MemberController.register()')

    @classmethod
    def update(cls):
        print('TODO: MemberController.update()')

    def list_all(self):
        self.view.list(self._members)

    def _filter(self, members):
        # TODO:  Return a subset of all members.
        return []
