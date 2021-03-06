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

from .. import exceptions
from . import encoding as enc


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


def makedirs(path):
    if not isinstance(path, bytes):
        raise TypeError('Expected "path" to be a bytestring path')
    if not path or not path.strip():
        raise ValueError('Got empty argument "path"')

    try:
        os.makedirs(enc.syspath(path))
    except (OSError, ValueError, TypeError) as e:
        raise exceptions.FilesystemError(e)


def delete(path, ignore_missing=False):
    """
    Deletes the file at "path".

    Args:
        path: The path to delete as an "internal bytestring".
        ignore_missing: Controls whether to ignore non-existent paths.
                        False: Non-existent paths raises 'FilesystemError'.
                        True: Non-existent paths are silently ignored.

    Raises:
        EncodingBoundaryViolation: Argument "path" is not of type 'bytes'.
        FilesystemError: The path could not be removed, or the path does not
                         exist and "ignore_missing" is False.
        ValueError: Argument "path" is empty or only whitespace.
    """
    if not path or not path.strip():
        raise ValueError('Argument "path" is empty or only whitespace')

    p = enc.syspath(path)
    if ignore_missing and not os.path.exists(p):
        return

    try:
        os.remove(enc.syspath(p))
    except OSError as e:
        raise exceptions.FilesystemError(e)
