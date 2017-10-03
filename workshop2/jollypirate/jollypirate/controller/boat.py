# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from copy import deepcopy

from jollypirate import exceptions
from jollypirate.controller.base import BaseController
from jollypirate.model import BoatModel
from jollypirate.view.base import MenuItem


class BoatController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        self.view.msg_boat_deletion_start()

        _boats = []
        _members = self.member_registry.getall()
        for m in _members:
            if m.boats:
                _boats.extend(m.boats)

        if not _boats:
            self.view.display_msg_failure('No boats have been registered!')
            self.view.msg_boat_deletion_failure()
            return

        _candidates = self._boats_as_menu_items(_boats)
        _boat_to_delete = self.view.get_selection_from(_candidates)
        if not _boat_to_delete:
            self.view.msg_boat_deletion_failure()
            return

        # TODO: Move mapping boat-owner-mapping to 'registry' ..
        _boat_owner = None
        for m in _members:
            if _boat_to_delete in m.boats:
                _boat_owner = m
                break

        if not _boat_owner:
            self.view.msg_boat_deletion_failure()
            return

        _boatless = deepcopy(_boat_owner)
        _boatless.remove_boat(_boat_to_delete)
        try:
            self.member_registry.remove(_boat_owner)
            self.member_registry.add(_boatless)
            self.member_registry.flush()
        except exceptions.JollyPirateModelError as e:
            self.view.display_msg_failure(str(e))
            self.view.msg_member_modify_failure()
        else:
            self.view.msg_boat_deletion_success()

    def register(self):
        self.view.msg_boat_registration_start()

        _new_boat = BoatModel()

        # Data validation is handled in the model.
        self.populate_model_data(
            _new_boat, model_field='type_', field_name='Boat Type'
        )
        self.populate_model_data(
            _new_boat, model_field='length', field_name='Length'
        )

        _members = self.member_registry.getall()
        _candidates = self._members_as_menu_items(_members)
        _selected_member = self.view.get_selection_from(_candidates)
        if not _selected_member:
            self.view.msg_boat_registration_failure()
            return

        # _boat_owner = deepcopy(_selected_member)
        # _boat_owner.add_boat(_new_boat)
        # self.member_registry.remove(_selected_member)
        # self.member_registry.add(_boat_owner)
        # self.member_registry.flush()

        _boat_owner = deepcopy(_selected_member)
        _boat_owner.add_boat(_new_boat)
        try:
            self.member_registry.remove(_selected_member)
            self.member_registry.add(_boat_owner)
        except exceptions.JollyPirateModelError as e:
            self.view.msg_boat_registration_failure()
            return
        else:
            self.view.msg_member_modify_success()

    def modify(self):
        self.view.msg_member_modify_start()

        _members = self.member_registry.getall()
        _candidates = self._members_as_menu_items(_members)
        _should_modify = self.view.get_selection_from(_candidates)
        if not _should_modify:
            self.view.msg_member_modify_failure()
            return

        _member = deepcopy(_should_modify)
        self.populate_model_data(
            _member, model_field='name_first', field_name='First Name'
        )
        self.populate_model_data(
            _member, model_field='name_last', field_name='Last Name'
        )
        self.populate_model_data(
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

    def populate_model_data(self, model_, model_field, field_name):
        _valid = False
        while not _valid:
            _user_input = self.view.get_field_data(field_name)
            try:
                setattr(model_, model_field, _user_input)
            except (exceptions.InvalidUserInput,
                    exceptions.JollyPirateModelError) as e:
                self.view.display_msg_failure(e)
                if self.view.should_abort():
                    return
            else:
                _valid = True

    def _boats_as_menu_items(self, boats):
        out = {}
        for i, boat in enumerate(boats):
            _description = '{!s} ({!s} meters)'.format(boat.type_, boat.length)
            _key = MenuItem(shortcut=self.int_to_char(i+1),
                            description=_description)
            out[_key] = boat
        return out
