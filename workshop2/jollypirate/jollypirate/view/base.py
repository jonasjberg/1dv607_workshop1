# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple
import logging

from jollypirate import exceptions
from jollypirate.util import (
    types,
    cli
)


MenuItem = namedtuple('MenuItem', ['shortcut', 'description'])


log = logging.getLogger()


CHAR_HEADING_UNDERLINE = '~'


class BaseView(object):

    def __init__(self):
        self.log = logging.getLogger(str(self))

    def display_menu(self, menu_items):
        self.display_msg_heading('Please Make a Selection')
        for item in menu_items:
            self._display_menu_entry(item.shortcut, item.description)

    @staticmethod
    def _display_menu_entry(shortcut, description):
        _s = '[{shortcut}]  {desc}'.format(shortcut=shortcut, desc=description)
        print(_s)

    @staticmethod
    def display_msg_heading(message):
        print('\n')
        print(message)
        print(CHAR_HEADING_UNDERLINE * len(message))
        print('')

    @staticmethod
    def display_msg_failure(message):
        _prefix = cli.colorize('[FAILURE]', fore='RED')
        print('{!s} {!s}'.format(_prefix, message))

    @staticmethod
    def display_msg_success(message):
        _prefix = cli.colorize('[SUCCESS]', fore='GREEN')
        print('{!s} {!s}'.format(_prefix, message))

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

