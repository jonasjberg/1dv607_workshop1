# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple
import logging

from jollypirate import exceptions
from jollypirate.util import types


MenuItem = namedtuple('MenuItem', ['shortcut', 'description'])


log = logging.getLogger()


class BaseView(object):
    def __init__(self):
        self.log = logging.getLogger(str(self))

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

    @staticmethod
    def display_error(message):
        print('[ERROR] {!s}'.format(message))

    @staticmethod
    def should_abort():
        while True:
            _raw_input = input('Abort? (y/[N])  ')
            string = types.force_string(_raw_input)
            if string:
                string = string.lower().strip()
                if string in ('y', 'j'):
                    return True
                if string in ('n', 'q'):
                    return False
            else:
                return False

    @staticmethod
    def get_non_empty_string():
        # Read input from stdin.
        _raw_input = input()

        # Coerce to the 'str' type. Failed coercion returns an empty string.
        string = types.force_string(_raw_input)
        if string.strip():
            return string.strip()
        else:
            raise exceptions.JollyPirateModelError(
                'Expected non-empty, not only whitespace string'
            )

    def __str__(self):
        return self.__class__.__name__

