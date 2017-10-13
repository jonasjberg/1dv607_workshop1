# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class JollyPirateException(Exception):
    """Base exception. All custom exceptions should subclass this."""


class InvalidUserInput(JollyPirateException):
    """Raised by views given invalid data from the user."""


class JollyPirateModelError(JollyPirateException):
    """Raised by models when provided unexpected data."""


class FilesystemError(JollyPirateException):
    """Errors occured while reading/writing files on disk. Should be used by
    the filesystem abstraction layer as a catch-all for failed operations."""


class DataPersistenceError(JollyPirateException):
    """Irrecoverable error while reading or writing data to disk."""
