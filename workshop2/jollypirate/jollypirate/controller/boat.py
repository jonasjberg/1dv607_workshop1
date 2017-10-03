# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate import exceptions
from jollypirate.controller.base import BaseController
from jollypirate.model import BoatModel
from jollypirate.view.base import MenuItem


class BoatController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        print('TODO: BoatController.delete()')

    def register(self):
        self.view.msg_boat_registration_start()

        _new_boat = BoatModel()

        # Data validation is handled in the model.
        self._populate_model_data(
            _new_boat, model_field='type_', field_name='Boat Type'
        )
        self._populate_model_data(
            _new_boat, model_field='length', field_name='Length'
        )

        _members = self.member_registry.getall()
        _candidates = self._members_as_menu_items(_members)
        _boat_owner = self.view.get_selection_from(_candidates)
        if not _boat_owner:
            self.view.msg_boat_registration_failure()
            return

        _boat_owner.add_boat(_new_boat)
        self.view.msg_boat_registration_success()

    def update(self):
        print('TODO: BoatController.register()')

    def _populate_model_data(self, model_, model_field, field_name):
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

