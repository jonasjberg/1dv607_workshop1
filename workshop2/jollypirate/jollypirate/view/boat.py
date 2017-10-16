# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .base import BaseView


class BoatView(BaseView):
    def __init__(self):
        super().__init__()

    def msg_boat_registration_start(self):
        self.display_msg_heading('Register a new Boat')

    def msg_boat_registration_success(self):
        self.display_msg_success('The new Boat has been Registered!')

    def msg_boat_registration_failure(self):
        self.display_msg_failure('The new Boat was NOT Registered ..')

    def msg_boat_deletion_start(self):
        self.display_msg_heading('Delete an existing Boat')

    def msg_boat_deletion_success(self):
        self.display_msg_success('The Boat has been Deleted!')

    def msg_boat_deletion_failure(self):
        self.display_msg_failure('The Boat was NOT Deleted ..')

    def msg_boat_modify_start(self):
        self.display_msg_heading('Modify an existing Boat')

    def msg_boat_modify_success(self):
        self.display_msg_success('The Boat has been Modified!')

    def msg_boat_modify_failure(self):
        self.display_msg_failure('The Boat was NOT Modified ..')
