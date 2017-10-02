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

import os
import re
import itertools
import logging

from . import encoding as enc


log = logging.getLogger(__name__)


# Needed by 'sanitize_filename' for sanitizing filenames in restricted mode.
ACCENT_CHARS = dict(zip('ÂÃÄÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖŐØŒÙÚÛÜŰÝÞßàáâãäåæçèéêëìíîïðñòóôõöőøœùúûüűýþÿ',
                        itertools.chain('AAAAAA', ['AE'], 'CEEEEIIIIDNOOOOOOO', ['OE'], 'UUUUUYP', ['ss'],
                                        'aaaaaa', ['ae'], 'ceeeeiiiionooooooo', ['oe'], 'uuuuuypy')))


def sanitize_filename(s, restricted=False, is_id=False):
    """Sanitizes a string so it could be used as part of a filename.
    If restricted is set, use a stricter subset of allowed characters.
    Set is_id if this is not an arbitrary string, but an ID that should be kept
    if possible.

    NOTE:  This function was lifted as-is from the "youtube-dl" project.

           https://github.com/rg3/youtube-dl/blob/master/youtube_dl/utils.py
           Commit: b407d8533d3956a7c27ad42cbde9a877c36df72c
    """
    def replace_insane(char):
        if restricted and char in ACCENT_CHARS:
            return ACCENT_CHARS[char]
        if char == '?' or ord(char) < 32 or ord(char) == 127:
            return ''
        elif char == '"':
            return '' if restricted else '\''
        elif char == ':':
            return '_-' if restricted else ' -'
        elif char in '\\/|*<>':
            return '_'
        if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
            return '_'
        if restricted and ord(char) > 127:
            return '_'
        return char

    # Handle timestamps
    s = re.sub(r'[0-9]+(?::[0-9]+)+', lambda m: m.group(0).replace(':', '_'), s)
    result = ''.join(map(replace_insane, s))
    if not is_id:
        while '__' in result:
            result = result.replace('__', '_')
        result = result.strip('_')
        # Common case of "Foreign band name - English song title"
        if restricted and result.startswith('-_'):
            result = result[2:]
        if result.startswith('-'):
            result = '_' + result[len('-'):]
        result = result.lstrip('.')
        if not result:
            result = '_'
    return result


def rename_file(source_path, new_basename):
    dest_base = enc.syspath(new_basename)
    source = enc.syspath(source_path)

    source = os.path.realpath(os.path.normpath(source))
    if not os.path.exists(source):
        raise FileNotFoundError('Source does not exist: "{!s}"'.format(
            enc.displayable_path(source)
        ))

    dest_abspath = os.path.normpath(
        os.path.join(os.path.dirname(source), dest_base)
    )
    if os.path.exists(dest_abspath):
        raise FileExistsError('Destination exists: "{!s}"'.format(
            enc.displayable_path(dest_abspath)
        ))

    log.debug('Renaming "{!s}" to "{!s}"'.format(
        enc.displayable_path(source),
        enc.displayable_path(dest_abspath))
    )
    try:
        os.rename(source, dest_abspath)
    except OSError:
        raise


def file_basename(file_path):
    return enc.syspath(os.path.basename(file_path))


CHAR_PERMISSION_LOOKUP = {
    'r': os.R_OK,
    'w': os.W_OK,
    'x': os.X_OK
}


def has_permissions(path, permissions):
    """
    Tests if a path has the specified permissions.

    The required permissions should be given as a single Unicode string.
    Examples:
                      Required      Required Permissions
                     Permissions    READ  WRITE  EXECUTE

                         'r'         X      -       -
                         'w'         -      X       -
                         'x'         -      -       X
                         'RW'        X      X       -
                         'WwxX'      -      X       X

    Args:
        path: The path to the file to test.
        permissions: The required permissions as a Unicode string
                             containing any of characters 'r', 'w' and 'x'.

    Returns:
        True if the given path has the given permissions, else False.
    """
    if not isinstance(permissions, str):
        raise TypeError('Expected "permissions" to be a Unicode string')
    if not isinstance(path, bytes):
        raise TypeError('Expected "path" to be a bytestring path')

    if not permissions.strip():
        return True

    perms = permissions.lower()
    for char in CHAR_PERMISSION_LOOKUP.keys():
        if char in perms:
            try:
                ok = os.access(enc.syspath(path), CHAR_PERMISSION_LOOKUP[char])
            except OSError:
                return False
            else:
                if not ok:
                    return False

    return True
