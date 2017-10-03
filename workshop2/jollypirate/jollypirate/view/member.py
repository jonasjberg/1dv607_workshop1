# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se
from jollypirate import exceptions
from .base import (
    BaseView,
    MenuItem
)


class MemberView(BaseView):
    def __init__(self):
        super().__init__()

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
        if callable(choice):
            choice(members)
        else:
            self.log.warning('Invalid selection: "{!s}"'.format(choice))

    def _list_verbose(self, members):
        print('TODO: view/member._list_verbose()')

    def _list_terse(self, members):
        print('TODO: view/member._list_terse()')

    def get_selection_from(self, menu_items):
        while True:
            self._print_menu(menu_items.keys())

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

    def _map_events_to_menuitem(self, events):
        return {
            menu_item: event
            for menu_item, event in self.menuitem_list_verbosity_map.items()
            if event in events
        }

    def get_member_field(self, field):
        _prompt = '[{}]:  '.format(field)
        return input(_prompt)

    def msg_member_registration_start(self):
        print('')
        print('Register new Member')
        print('~~~~~~~~~~~~~~~~~~~')
        print('')
