# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .base import BaseModel
from .member import MemberModel
from .. import (
    exceptions,
    persistence
)
from jollypirate.exceptions import DataPersistenceError


class MemberRegistry(BaseModel):
    STORAGE_KEY = 'registry'

    def __init__(self):
        super().__init__()

        self._members = set()
        try:
            self._persistence = persistence.get_implementation(self.STORAGE_KEY)
        except DataPersistenceError as e:
            raise exceptions.JollyPirateException(e)

        try:
            _stored_data = self._persistence.get('members')
        except KeyError as e:
            self.log.error('Error when reading persistent data; {!s}'.format(e))
        else:
            self.log.debug(
                'Loaded persistent data ({!s}) {!s}'.format(type(_stored_data),
                                                            _stored_data)
            )

            _stored_members = _stored_data.get('all')
            if _stored_members:
                self.log.debug('Got {!s} member(s) from persistent data'.format(
                        len(_stored_members)
                ))
                for _member in _stored_members:
                    self.log.debug('Loaded member "{!r}"'.format(_member))
                    self._members.add(_member)
            else:
                self.log.debug('Got no members from persistent data')

            # self._members.union()

    def add(self, new_member):
        if not isinstance(new_member, MemberModel):
            raise exceptions.JollyPirateModelError(
                'Expected an instance of "MemberModel"'
            )

        if new_member in self._members:
            raise exceptions.JollyPirateModelError(
                'Member "{!s}" is already in {}'.format(new_member, self)
            )

        self._members.add(new_member)
        self._update_persistent_data()

    def remove(self, member_to_remove):
        if not self.contains(member_to_remove):
            raise exceptions.JollyPirateModelError(
                'The specified member is not registered'
            )

        self._members.remove(member_to_remove)
        self.log.debug('Removed member "{!r}"'.format(member_to_remove))
        self._update_persistent_data()

    def contains(self, member):
        if not isinstance(member, MemberModel):
            return False

        return bool(
            any(member.id == member.id for member in self._members)
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

    def getall_boatowners(self):
        return [m for m in self._members if m.boats]

    def getowner(self, boat):
        for _member in self.getall():
            if boat in _member.boats:
                return _member
        return None

    def flush(self):
        self._update_persistent_data()

    def _update_persistent_data(self):
        _data = {'all': self.getall()}
        self.log.debug(
            'Updating persistent data ({!s}) {!s}'.format(type(_data), _data)
        )
        self._persistence.set('members', _data)
