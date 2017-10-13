# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple
import logging

from .. import exceptions
from ..util import (
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

    @classmethod
    def should_abort(cls):
        while True:
            _raw_input = cls.get_user_input(message='Abort? (y/[N])  ')
            string = types.force_string(_raw_input)
            if string:
                string = string.lower().strip()
                if string in ('y', 'j'):
                    return True
                if string in ('n', 'q'):
                    return False
            else:
                return False

    @classmethod
    def force_non_empty_string(cls, raw_input):
        # Coerce to the 'str' type. Failed coercion returns an empty string.
        string = types.force_string(raw_input)
        if string.strip():
            # Strip any leading/trailing whitespace.
            return string.strip()
        else:
            raise exceptions.InvalidUserInput(
                'Expected non-empty and not only whitespace string. '
                'Got "{!s}"'.format(string)
            )

    @classmethod
    def get_user_input(cls, message=None):
        if not message:
            message = 'INPUT: '

        # Read input from stdin.
        try:
            return input(message)
        except Exception:
            raise exceptions.InvalidUserInput

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def get_field_data(cls, field, should_choose_one_of=None):
        if should_choose_one_of:
            # Include comma-separated elements in 'should_choose_one_of'.
            alternatives = ', '.join(str(a) for a in should_choose_one_of)
            _prompt_message = '[{}] ({}):  '.format(field, alternatives)
        else:
            _prompt_message = '[{}]:  '.format(field)

        return cls.get_user_input(_prompt_message)

