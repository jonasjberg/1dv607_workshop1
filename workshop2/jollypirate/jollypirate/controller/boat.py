# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .. import exceptions
from ..controller import BaseController
from ..model import (
    BoatModel,
    MemberModel
)
from ..view import MenuItem


class BoatController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        self.view.msg_boat_deletion_start()

        _boats = []
        _members = self.member_registry.getall_boatowners()
        for m in _members:
            _boats.extend(m.boats)

        if not _boats:
            self.view.display_msg_failure('No boats have been registered!')
            self.view.msg_boat_deletion_failure()
            return

        _menu_items = self._boats_as_menu_items(_boats)
        _boat_to_delete = self.view.get_selection_from(_menu_items)
        if not _boat_to_delete:
            self.view.msg_boat_deletion_failure()
            return

        _boat_owner = self.member_registry.getowner(_boat_to_delete)
        if not _boat_owner:
            self.view.msg_boat_deletion_failure()
            return

        _boatless = MemberModel.copy(_boat_owner)
        _boatless.remove_boat(_boat_to_delete)
        try:
            self.member_registry.remove(_boat_owner)
            self.member_registry.add(_boatless)
        except exceptions.JollyPirateModelError as e:
            self.view.display_msg_failure(str(e))
            self.view.msg_boat_modify_failure()
        else:
            self.view.msg_boat_deletion_success()

    def register(self):
        self.view.msg_boat_registration_start()

        _new_boat = BoatModel()

        # Data validation is handled in the model.
        self.populate_model_data(
            _new_boat, model_field='type_', field_name='Boat Type',
            should_choose_one_of=self.model.BOAT_TYPES.all()
        )
        self.populate_model_data(
            _new_boat, model_field='length', field_name='Length'
        )

        _members = self.member_registry.getall()
        _menu_items = self._members_as_menu_items(_members)
        _selected_member = self.view.get_selection_from(_menu_items)
        if not _selected_member:
            self.view.msg_boat_registration_failure()
            return

        _boat_owner = MemberModel.copy(_selected_member)
        _boat_owner.add_boat(_new_boat)
        try:
            self.member_registry.remove(_selected_member)
            self.member_registry.add(_boat_owner)
        except exceptions.JollyPirateModelError:
            self.view.msg_boat_registration_failure()
            return
        else:
            self.view.msg_boat_registration_success()

    def modify(self):
        self.view.msg_boat_modify_start()

        _all_boats = []
        _members = self.member_registry.getall_boatowners()
        for m in _members:
            _all_boats.extend(m.boats)

        if not _all_boats:
            self.view.display_msg_failure('No boats have been registered!')
            self.view.msg_boat_modify_failure()
            return

        _menu_items = self._boats_as_menu_items(_all_boats)
        _boat_to_modify = self.view.get_selection_from(_menu_items)
        if not _boat_to_modify:
            self.view.msg_boat_modify_failure()
            return

        _boat_owner = self.member_registry.getowner(_boat_to_modify)
        if not _boat_owner:
            self.view.msg_boat_modify_failure()
            return

        _owner_copy = MemberModel.copy(_boat_owner)

        _new_boat = BoatModel()
        self.populate_model_data(
            _new_boat, model_field='type_', field_name='Boat Type',
            should_choose_one_of=self.model.BOAT_TYPES.all()
        )
        self.populate_model_data(
            _new_boat, model_field='length', field_name='Length'
        )

        if _new_boat:
            _owner_copy.remove_boat(_boat_to_modify)
            _owner_copy.add_boat(_new_boat)
            try:
                self.member_registry.remove(_boat_owner)
                self.member_registry.add(_owner_copy)
            except exceptions.JollyPirateModelError as e:
                self.view.display_msg_failure(str(e))
                self.view.msg_boat_modify_failure()
            else:
                self.view.msg_boat_modify_success()

    def _boats_as_menu_items(self, boats):
        out = {}
        for i, boat in enumerate(boats):
            _description = '{!s} ({!s} meters)'.format(boat.type_, boat.length)
            _key = MenuItem(shortcut=self.int_to_char(i+1),
                            description=_description)
            out[_key] = boat
        return out
