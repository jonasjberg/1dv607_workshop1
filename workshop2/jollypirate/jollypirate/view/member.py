# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate import exceptions
from jollypirate.util.cli import ColumnFormatter
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
                shortcut='b', description='Compact Listing'
            ): self._list_compact,
        }

    def list(self, members):
        lister = self.get_selection_from(self.menuitem_list_verbosity_map)
        if callable(lister):
            lister(members)
        else:
            self.log.warning('Invalid selection: "{!s}"'.format(lister))

    def _list_verbose(self, members):
        cf = ColumnFormatter()
        cf.addrow('First Name', 'Last Name', 'Social Security Number', 'Member ID')
        cf.addrow('==========', '=========', '======================', '=========')
        cf.setalignment('left', 'left', 'right', 'right')

        for m in members:
            cf.addrow(
                m.name_first, m.name_last, m.social_sec_number, str(m.id)[1:10]
            )

            # TODO: List any boats and boat information.

        print('\n\nDetailed Listing of all Registered Members:\n')
        print(str(cf))

    def _list_compact(self, members):
        # name, id, num boats
        cf = ColumnFormatter()
        cf.addrow('Name', 'Member ID')
        cf.addrow()
        print('TODO: view/member._list_compact()')

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
        self.display_msg_heading('Register new Member')

    def msg_member_registration_success(self):
        self.display_msg_success('The new member has been registered!')

    def msg_member_registration_failure(self):
        self.display_msg_success('The member has not been registered ..')
