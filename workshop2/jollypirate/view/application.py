# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class ApplicationView(object):
    def __init__(self):
        pass

    def get_selection_from(self, menu_choices):
        choice = None

        while not choice or choice.lower() not in menu_choices.keys():
            self._print_choices(menu_choices)
            _choice = input()
            try:
                string_choice = str(_choice)
            except (ValueError, TypeError):
                pass
            else:
                if string_choice:
                    return string_choice

    def _print_choices(self, menu_choices):
        print('Make a selection:')
        for key, description in menu_choices.items():
            self._print_choice(key, description)

    @staticmethod
    def _print_choice(key, description):
        _s = '[{key}]     {desc}'.format(key=key, desc=description)
        print(_s)
