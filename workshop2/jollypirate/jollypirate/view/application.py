# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple
import logging

from jollypirate.controller import Events


log = logging.getLogger(__name__)


MenuItem = namedtuple('MenuItem', ['shortcut', 'description'])


class ApplicationView(object):
    def __init__(self):
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
            ): Events.BOAT_UPDATE,
            MenuItem(
                shortcut='u', description='Delete a Member'
            ): Events.MEMBER_DELETE,
            MenuItem(
                shortcut='j', description='Get Information on a Specific Member'
            ): Events.MEMBER_INFOQUERY,
            MenuItem(
                shortcut='m', description='Register a Member'
            ): Events.MEMBER_REGISTER,
            MenuItem(
                shortcut='k', description='Update a Member'
            ): Events.MEMBER_UPDATE,
            MenuItem(
                shortcut='l', description='List all Members'
            ): Events.MEMBERS_LIST,
        }

    def get_selection_from(self, events):
        # Get menu items that are mapped to an event in argument "events".
        _menu_items_to_include = self._map_events_to_menuitem(events)

        while True:
            self._print_menu(_menu_items_to_include)

            # Read input from stdin.
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
                for menu_item, event in _menu_items_to_include.items():
                    if choice == menu_item.shortcut:
                        log.debug('Valid choice: {!s}'.format(choice))
                        return event

                log.debug('Invalid Selection')

    def _map_events_to_menuitem(self, events):
        return {
            menu_item: event
            for menu_item, event in self.menuitems_event_map.items()
            if event in events
        }

    def _print_menu(self, menu_items):
        print('\n\n')
        print('Please Make a Selection')
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        for item in menu_items.keys():
            self._print_menu_entry(item.shortcut, item.description)

    @staticmethod
    def _print_menu_entry(shortcut, description):
        _s = '[{shortcut}]  {desc}'.format(shortcut=shortcut, desc=description)
        print(_s)
