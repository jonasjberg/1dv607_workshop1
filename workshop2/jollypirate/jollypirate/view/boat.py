# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate.view.base import BaseView


class BoatView(BaseView):
    def __init__(self):
        super().__init__()

    def get_selection_from(self, menu_items):
        while True:
            self.display_menu(menu_items.keys())

            _choice = input()
            try:
                # Coerce the input to type str.
                choice = str(_choice)
            except (ValueError, TypeError):
                # Silently ignore failed coercion.
                pass
            else:
                # Make lower case and strip any leading/trailing whitespace.
                choice = choice.lower().strip()

                # Return the event associated with the users choice, if any.
                for menu_item, handler in menu_items.items():
                    if choice == menu_item.shortcut:
                        self.log.debug('Valid choice: {!s}'.format(choice))
                        return handler

            self.log.debug('Invalid Selection')

    def msg_boat_registration_start(self):
        self.display_msg_heading('Register a new Boat')

    def msg_boat_registration_success(self):
        self.display_msg_success('The new Boat has been Registered!')

    def msg_boat_registration_failure(self):
        self.display_msg_failure('The new Boat has been Registered!')

    def msg_boat_deletion_start(self):
        self.display_msg_heading('Delete an existing Boat')

    def msg_boat_deletion_success(self):
        self.display_msg_success('The Boat has been Deleted!')

    def msg_boat_deletion_failure(self):
        self.display_msg_failure('The Boat was NOT Deleted ..')


