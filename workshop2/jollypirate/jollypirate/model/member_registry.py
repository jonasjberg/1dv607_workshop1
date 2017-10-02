# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate.model import MemberModel


class MemberRegistry(object):
    def __init__(self):
        self._members = set()

    def add(self, new_member):
        if not isinstance(new_member, MemberModel):
            raise TypeError('Expected an instance of "MemberModel"')

        if new_member in self._members:
            raise ValueError(
                'Member "{!s}" is already in {}'.format(new_member, self)
            )

        self._members.add(new_member)

    def remove(self, member_to_remove):
        self._members.remove(member_to_remove)

    def contains(self, member_id):
        return bool(
            any(member.id == member_id for member in self._members)
        )

    def get(self, member_id):
        if not self.contains(member_id):
            return None

        for member in self._members:
            if member.id == member_id:
                return member

        return None


