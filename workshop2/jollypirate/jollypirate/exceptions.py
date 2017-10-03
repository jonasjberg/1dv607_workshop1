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
