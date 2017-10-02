# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple


MenuItem = namedtuple('MenuItem', ['shortcut', 'description'])


class BaseView(object):
    def __init__(self):
        pass

    def _print_menu(self, menu_items):
        print('\n\n')
        print('Please Make a Selection')
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        for item in menu_items:
            self._print_menu_entry(item.shortcut, item.description)

    @staticmethod
    def _print_menu_entry(shortcut, description):
        _s = '[{shortcut}]  {desc}'.format(shortcut=shortcut, desc=description)
        print(_s)
