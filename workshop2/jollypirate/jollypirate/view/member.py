# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging

from .base import (
    BaseView,
    MenuItem
)


log = logging.getLogger(__name__)


class MemberView(BaseView):
    def __init__(self):
        super(MemberView).__init__()

        self.menuitem_list_verbosity_map = {
            MenuItem(
                shortcut='v', description='Verbose Listing'
            ): self._list_verbose,
            MenuItem(
                shortcut='b', description='Terse Listing'
            ): self._list_terse,
        }

    def list(self, members):
        choice = self.get_selection_from(self.menuitem_list_verbosity_map)
        _method = getattr(self, choice)
        if callable(_method):
            _method(members)

    def _list_verbose(self, members):
        print('TODO: view/member._list_verbose()')

    def _list_terse(self, members):
        print('TODO: view/member._list_terse()')

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
            for menu_item, event in self.menuitem_list_verbosity_map.items()
            if event in events
        }
