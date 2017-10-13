# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .. import exceptions
from .base import (
    BaseView,
    MenuItem
)
from ..controller.event import Events


class ApplicationView(BaseView):
    def __init__(self):
        super().__init__()

        self.menuitems_event_map = {
            MenuItem(
                shortcut='q', description='Exit Program'
            ): Events.APP_QUIT,
            MenuItem(
                shortcut='t', description='Delete a Boat'
            ): Events.BOAT_DELETE,
            MenuItem(
                shortcut='g', description='Register a Boat'
            ): Events.BOAT_REGISTER,
            MenuItem(
                shortcut='b', description='Update a Boat'
            ): Events.BOAT_MODIFY,
            MenuItem(
                shortcut='u', description='Delete a Member'
            ): Events.MEMBER_DELETE,
            MenuItem(
                shortcut='j', description='Get Information on a Specific Member'
            ): Events.MEMBER_LIST,
            MenuItem(
                shortcut='m', description='Register a Member'
            ): Events.MEMBER_REGISTER,
            MenuItem(
                shortcut='k', description='Update a Member'
            ): Events.MEMBER_MODIFY,
            MenuItem(
                shortcut='l', description='List all Members'
            ): Events.MEMBER_LISTALL,
        }

    def get_selection_from(self, events):
        # Get menu items that are mapped to an event in argument "events".
        _menu_items_to_include = self._map_events_to_menuitem(events)

        while True:
            self.display_menu(_menu_items_to_include.keys())

            # Read input from stdin.
            try:
                _choice = self.get_user_input()
            except exceptions.InvalidUserInput:
                continue

            try:
                # Coerce the input to type str.
                choice = self.force_non_empty_string(_choice)
            except exceptions.InvalidUserInput as e:
                # Silently ignore failed coercion, include only in debug log.
                self.log.debug(str(e))
            else:
                # Transform string to lower-case.
                choice = choice.lower()

                # Return the event associated with the users choice, if any.
                for menu_item, event in _menu_items_to_include.items():
                    if choice == menu_item.shortcut:
                        self.log.debug('Valid choice: {!s}'.format(choice))
                        return event

            self.log.debug('Invalid Selection')

    def _map_events_to_menuitem(self, events):
        return {
            menu_item: event
            for menu_item, event in self.menuitems_event_map.items()
            if event in events
        }

    def msg_application_start(self):
        self.display_msg_success(
            'Started the Jolly Pirate Boat Club Management Suite'
        )

    def msg_application_success(self):
        print('\n')
        self.display_msg_success('Exiting successfully! ')

    def msg_application_failure(self):
        print('\n')
        self.display_msg_failure('Exiting with ERRORS ..')
