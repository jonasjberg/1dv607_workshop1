# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from ..util import cli
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
                shortcut='c', description='Compact Listing'
            ): self._list_compact,
        }

    def list(self, members):
        lister = self.get_selection_from(self.menuitem_list_verbosity_map)
        if callable(lister):
            lister(members)
        else:
            self.log.warning('Invalid selection: "{!s}"'.format(lister))

    def _list_verbose(self, members):
        cf = cli.ColumnFormatter()
        cf.addrow(
            'First Name', 'Last Name', 'Social Security Number', 'Member ID'
        )
        cf.addrow(*['=' * width for width in cf.column_widths])
        cf.setalignment('left', 'left', 'right', 'right')

        for m in members:
            cf.addrow(
                m.name_first, m.name_last, m.social_sec_number, str(m.id)[1:10]
            )

            _boats = m.boats
            if _boats:
                cf.addemptyrow()

                cf.addrow(None, 'Boat Type', 'Boat Length', None)
                cf.addrow(None, '=========', '===========', None)
                for b in _boats:
                    cf.addrow(None, b.type_, str(b.length), None)

                cf.addrow(*['_' * width for width in cf.column_widths])
                cf.addemptyrow()

        self.display_msg_heading('Detailed Listing of all Registered Members:')
        print(str(cf))
        print('\n')

    def _list_compact(self, members):
        # name, id, num boats
        cf = cli.ColumnFormatter()
        cf.addrow('Name', 'Member ID', '#Boats')
        cf.addrow(*['=' * width for width in cf.column_widths])

        for m in members:
            _full_name = '{!s} {!s}'.format(m.name_first, m.name_last)
            cf.addrow(_full_name, str(m.id)[1:10], str(len(m.boats)))

        self.display_msg_heading('Compact Listing of all Registered Members:')
        print(str(cf))
        print('\n')

    def _map_events_to_menuitem(self, events):
        return {
            menu_item: event
            for menu_item, event in self.menuitem_list_verbosity_map.items()
            if event in events
        }

    def msg_member_registration_start(self):
        self.display_msg_heading('Register a new Member')

    def msg_member_registration_success(self):
        self.display_msg_success('The new Member has been Registered!')

    def msg_member_registration_failure(self):
        self.display_msg_success('The Member has NOT been Registered ..')

    def msg_member_deletion_start(self):
        self.display_msg_heading('Delete an existing Member')

    def msg_member_deletion_success(self):
        self.display_msg_success('The Member has been Deleted!')

    def msg_member_deletion_failure(self):
        self.display_msg_failure('No Member was Deleted ..')

    def msg_member_modify_start(self):
        self.display_msg_heading('Modify an existing Member')

    def msg_member_modify_success(self):
        self.display_msg_success('The Member has been Modified!')

    def msg_member_modify_failure(self):
        self.display_msg_failure('The Member was NOT Modified ..')

    def msg_member_info_start(self):
        self.display_msg_heading('Get information about a Specific Member')

    def msg_member_info_success(self):
        self.display_msg_success('The information was provided!')

    def msg_member_info_failure(self):
        self.display_msg_failure('Requested information was NOT provided ..')

    def display_member_info(self, member):
        cf = cli.ColumnFormatter()
        cf.addrow(
            'First Name', 'Last Name', 'Social Security Number', 'Member ID',
            '# Boats'
        )
        cf.addrow(*['=' * width for width in cf.column_widths])
        cf.setalignment('left', 'left', 'right', 'right', 'left')
        cf.addrow(
            member.name_first, member.name_last, member.social_sec_number,
            str(member.id)[1:10], str(len(member.boats))
        )

        self.display_msg_heading('Information on Specified Member:')
        print(str(cf))
        print('\n')
