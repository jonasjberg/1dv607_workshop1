# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging

from jollypirate import persistence
from jollypirate.model import MemberModel


log = logging.getLogger(__name__)


class MemberRegistry(object):
    STORAGE_KEY = 'registry'

    def __init__(self):
        self._members = set()
        self._persistence = persistence.get_implementation(self.STORAGE_KEY)

        try:
            _stored_data = self._persistence.get('members')
        except KeyError as e:
            log.error('Error when reading persistent data; {!s}'.format(e))
        else:
            log.debug('Loaded persistent data:')
            log.debug(str(_stored_data))
            # _stored_members =

            # self._members.union()

    def add(self, new_member):
        if not isinstance(new_member, MemberModel):
            raise TypeError('Expected an instance of "MemberModel"')

        if new_member in self._members:
            raise ValueError(
                'Member "{!s}" is already in {}'.format(new_member, self)
            )

        self._members.add(new_member)
        self._update_persistent_data()

    def remove(self, member_to_remove):
        self._members.remove(member_to_remove)
        self._update_persistent_data()

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

    def getall(self):
        return list(self._members)

    def _update_persistent_data(self):
        self._persistence.set(self.STORAGE_KEY, {'members': self.getall()})
