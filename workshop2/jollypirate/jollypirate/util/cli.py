#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright(c) 2016-2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se
#
#   This file is part of autonameow.
#
#   autonameow is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation.
#
#   autonameow is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with autonameow.  If not, see <http://www.gnu.org/licenses/>.

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None


CLI_MSG_HEADING_CHAR = '~'


def colorize(text, fore=None, back=None, style=None):
    """
    Adds ANSI formatting to text strings with "colorama".

    The text is returned as-is if the top-level import of "colorama" failed.

    Refer the "colorama" library documentation for additional information;
        https://pypi.python.org/pypi/colorama

    Args:
        text: The text to colorize.
        fore: Optional foreground color as a string. Available options;
              BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
              LIGHTBLACK_EX, LIGHTRED_EX, LIGHTGREEN_EX, LIGHTYELLOW_EX
              LIGHTBLUE_EX, LIGHTMAGENTA_EX, LIGHTCYAN_EX, LIGHTWHITE_EX
        back: Optional background color as a string. Available options;
              BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,
              LIGHTBLACK_EX, LIGHTRED_EX LIGHTGREEN_EX, LIGHTYELLOW_EX,
              LIGHTBLUE_EX, LIGHTMAGENTA_EX, LIGHTCYAN_EX, LIGHTWHITE_EX
        style: Optional style settings as a string. Available options;
               DIM, NORMAL, BRIGHT, RESET_ALL

    Returns:
        The given string with the specified coloring and style options applied.
        If no options are specified or if "colorama" is not available, the
        text is returned as-is. If "text" is None, an empty string is returned.
    """
    if text is None:
        return ''
    if not (fore or back or style) or not colorama:
        return text

    buffer = []

    if fore:
        buffer.append(getattr(colorama.Fore, fore.upper(), None))
    if back:
        buffer.append(getattr(colorama.Back, back.upper(), None))
    if style:
        buffer.append(getattr(colorama.Style, style.upper(), None))

    buffer.append(text)

    if style:
        buffer.append(colorama.Style.RESET_ALL)
    if back:
        buffer.append(colorama.Back.RESET)
    if fore:
        buffer.append(colorama.Fore.RESET)

    return ''.join(buffer)


def msg(message, style=None):
    """
    Displays a message to the user using preset formatting options.

    Args:
        message: The raw text message to print as a string.
        style: Optional message type.
    """
    def print_default_msg(text):
        print(colorize(text))

    def print_info_msg(text):
        prefix = colorize('[info]', fore='LIGHTBLACK_EX')
        colored_text = colorize(text)
        print(prefix + ' ' + colored_text)

    if not message:
        return

    if not style:
        print_default_msg(message)

    elif style == 'info':
        print_info_msg(message)

    elif style == 'heading':
        _heading_underline = CLI_MSG_HEADING_CHAR * len(message)
        _colored_heading_underline = colorize(_heading_underline, style='DIM')
        _colored_heading_text = colorize(message, style='BRIGHT')
        print('\n')
        print(_colored_heading_text)
        print(_colored_heading_underline)

    else:
        print_default_msg(message)


class ColumnFormatter(object):
    """
    Utility formatter for aligning columns of strings.
    The individual column widths are expanded dynamically when
    strings are added. New strings are added a column at a time.

    Each column width is as wide as the widest string contained
    in that column + 'COLUMN_PADDING'.

    Example Usage:    ColumnFormatter cf = ColumnFormatter()
                      cf.addrow('foo', 'bar')
                      cf.addrow('MJAO OAJM', 'baz')
                      cf.addrow('1337', '4E4F4F42')
                      print(str(cf))

    Which would print something like:              foo        bar
                                                   MJAO OAJM  baz
                                                   1337       4E4F4F42

    With 'cf.setalignment('right', 'left'):              foo  bar
                                                   MJAO OAJM  baz
                                                        1337  4E4F4F42
    """
    COLUMN_PADDING = 2
    PADDING_CHAR = ' '
    ALIGNMENT_STRINGS = {
        'left': 'ljust',
        'right': 'rjust'
    }

    def __init__(self, align='left'):
        self._column_count = 0
        self._data = []
        self._column_widths = []
        self._default_align = self.ALIGNMENT_STRINGS.get(align, 'ljust')
        self._column_align = []

    def setalignment(self, *args):
        maybe_strings = list(args)
        strings = self._check_types_replace_none(maybe_strings)
        if not strings:
            return

        _column_alignment = []
        for i in range(0, self.number_columns):
            if i < len(strings) and [s in self.ALIGNMENT_STRINGS.keys()
                                     for s in strings]:
                _column_alignment.append(self.ALIGNMENT_STRINGS.get(strings[i]))
            else:
                _column_alignment.append(self._default_align)

        self._column_align = _column_alignment

    @property
    def alignment(self):
        if not self._column_align:
            out = []
            out.extend(self._default_align for _ in range(self.number_columns))
            return out
        else:
            return self._column_align

    @property
    def number_columns(self):
        return self._column_count

    def _update_number_columns(self, strings):
        count = len(strings)
        if count > self._column_count:
            self._column_count = count

    def addrow(self, *args):
        maybe_strings = list(args)

        strings = self._check_types_replace_none(maybe_strings)

        self._update_number_columns(strings)
        self._update_column_widths(strings)
        self._data.append(strings)

    def addemptyrow(self):
        self.addrow(' ')

    def _update_column_widths(self, strings):
        # strings = [textutils.strip_ansiescape(s) for s in strings]
        # strings = [textutils.normalize_unicode(s) for s in strings]
        new_widths = [len(s) for s in strings]

        if not self._column_widths:
            self._column_widths = new_widths
        else:
            new_column_count = len(new_widths)
            old_column_count = len(self._column_widths)

            # Use the longest array as the "base".
            if new_column_count > old_column_count:
                _max_widths = new_widths
            else:
                _max_widths = self._column_widths

            #   Array A:   [9]  [1]
            #   Array B:   [3]  [7]  [2]  [4]
            #       OUT:   [9]  [7]  [2]  [4]
            #
            # Compare array elements from index 0..len(A) and store the
            # maximum element value in the longer array.
            for i in range(0, min(new_column_count, old_column_count)):
                _max_widths[i] = max(new_widths[i], self._column_widths[i])

            self._column_widths = _max_widths

    @property
    def column_widths(self):
        return self._column_widths

    def max_column_width(self):
        max_width = ((self.number_columns * self.COLUMN_PADDING)
                     + sum(self.column_widths) - self.COLUMN_PADDING)
        return max_width

    @staticmethod
    def _check_types_replace_none(maybe_strings):
        out = []

        if not maybe_strings:
            return out

        for _element in maybe_strings:
            if _element is None:
                out.append('')
            elif not isinstance(_element, str):
                raise TypeError(
                    'Expected Unicode str. Got "{!s}"'.format(type(_element))
                )
            else:
                out.append(_element.strip())

        return out

    def __str__(self):
        if not self._data:
            return ''

        padding = self.PADDING_CHAR * self.COLUMN_PADDING

        lines = []
        for row in self._data:
            lines.append(
                padding.join(
                    getattr(word, align)(width)
                    for word, width, align in zip(
                        row, self._column_widths,
                        self.alignment
                    )
                )
            )

        return '\n'.join(l.rstrip() for l in lines)
