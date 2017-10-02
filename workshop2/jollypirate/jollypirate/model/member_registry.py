# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class MemberRegistry(object):
    def __init__(self):
        self._members = set()

    def add(self, new_member):
        self._members.add(new_member)

    def remove(self, member_to_remove):
        self._members.remove(member_to_remove)

    def get(self, member_id):
        self._members.remove(new_member)


