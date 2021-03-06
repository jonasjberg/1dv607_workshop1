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

"""
Custom data types, used internally by autonameow.
Coerces incoming data with unreliable or unknown types to primitives.
Provides "NULL" values and additional type-specific functionality.

Use by passing data through the singletons defined at the bottom of this file.
The values are "passed through" the type classes and returned as primitive or
standard library types (E.G. "datetime").
These classes are meant to be used as "filters" for coercing values to known
types --- they are shared and should not retain any kind of state.
"""

import os
import re

from . import encoding


class AWTypeError(Exception):
    """Failure to coerce a value with one of the type coercers."""


class BaseType(object):
    """
    Base class for all custom types. Provides type coercion and known defaults.
    Does not store values -- intended to act as filters.
    """
    # Default "None" value to fall back to.
    NULL = 'NULL'

    # Types that can be coerced with the 'coerce' method.
    COERCIBLE_TYPES = (str,)

    # Used by the 'equivalent' method to check if types are "equivalent".
    EQUIVALENT_TYPES = (str, )

    def __call__(self, value=None):
        if value is None:
            return self.null()
        elif self.equivalent(value):
            # Pass through if type is "equivalent" without coercion.
            return value
        elif self.acquiescent(value):
            # Type can be coerced, check after coercion to make sure.
            value = self.coerce(value)
            if self.equivalent(value):
                return value

        self._fail_coercion(value)

    def null(self):
        return self.NULL

    def equivalent(self, value):
        return isinstance(value, self.EQUIVALENT_TYPES)

    def acquiescent(self, value):
        return isinstance(value, self.COERCIBLE_TYPES)

    def coerce(self, value):
        """
        Coerces values whose types are included in 'COERCIBLE_TYPES'.

        If the value is not part of the specific class 'COERCIBLE_TYPES',
        the coercion fails and a class-specific "null" value is returned.

        Args:
            value: The value to coerce as any type, including None.

        Returns:
            A representation of the original value coerced to the type
            represented by the specific class, or the class "null" value if
            coercion fails.

        Raises:
            AWTypeError: The value could not be coerced.
        """
        raise NotImplementedError('Must be implemented by inheriting classes.')

    def normalize(self, value):
        """
        Processes the given value to a form suitable for serialization/storage.

        Calling this method should be equivalent to calling 'coerce' followed
        by some processing that produces a "simplified" representation of
        the value.  Strings might be converted to lower-case, etc.

        Args:
            value: The value to coerce as any type, including None.

        Returns:
            A "normalized" version of the given value if the value can be
            coerced and normalized, or the class "null" value.

        Raises:
            AWTypeError: The value could not be coerced and/or normalized.
        """
        raise NotImplementedError('Must be implemented by inheriting classes.')

    def format(self, value, **kwargs):
        raise NotImplementedError('Must be implemented by inheriting classes.')

    def _fail_normalization(self, value, msg=None):
        error_msg = 'Unable to normalize "{!s}" into {!r}'.format(value, self)
        if msg is not None:
            error_msg = '{}; {!s}'.format(error_msg, msg)

        raise AWTypeError(error_msg)

    def _fail_coercion(self, value, msg=None):
        error_msg = 'Unable to coerce "{!s}" into {!r}'.format(value, self)
        if msg is not None:
            error_msg = '{}; {!s}'.format(error_msg, msg)

        raise AWTypeError(error_msg)

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Path(BaseType):
    COERCIBLE_TYPES = (str, bytes)

    # Always force coercion so that all incoming data is properly normalized.
    EQUIVALENT_TYPES = ()

    # Make sure to never return "null" -- raise a 'AWTypeError' exception.
    NULL = 'INVALID PATH'

    def __call__(self, value=None):
        # Overrides the 'BaseType' __call__ method as to not perform the test
        # after the the value coercion. This is because the path could be a
        # byte string and still not be properly normalized.
        if value is not None and self.acquiescent(value):
            if value.strip() is not None:
                value = self.coerce(value)
                return value

        self._fail_coercion(value)

    def coerce(self, value):
        if value:
            try:
                return encoding.bytestring_path(value)
            except (ValueError, TypeError):
                pass

        self._fail_coercion(value)

    def normalize(self, value):
        value = self.__call__(value)
        if value:
            return encoding.normpath(value)

        self._fail_normalization(value)

    def format(self, value, **kwargs):
        parsed = self.__call__(value)
        return encoding.displayable_path(parsed)


class PathComponent(BaseType):
    COERCIBLE_TYPES = (str, bytes)
    EQUIVALENT_TYPES = (bytes, )
    NULL = b''

    def coerce(self, value):
        try:
            return encoding.bytestring_path(value)
        except (ValueError, TypeError):
            self._fail_coercion(value)

    def normalize(self, value):
        value = self.__call__(value)
        if value:
            # Expand user home directory if present.
            return os.path.normpath(os.path.expanduser(encoding.syspath(value)))

        self._fail_normalization(value)

    def format(self, value, **kwargs):
        value = self.__call__(value)
        return encoding.displayable_path(value)


class Boolean(BaseType):
    COERCIBLE_TYPES = (bytes, str, int, float, object)
    EQUIVALENT_TYPES = (bool, )
    NULL = False

    STR_TRUE = frozenset('positive true yes'.split())
    STR_FALSE = frozenset('negative false no'.split())

    def string_to_bool(self, string_value):
        value = string_value.lower().strip()
        if value in self.STR_TRUE:
            return True
        if value in self.STR_FALSE:
            return False

    @staticmethod
    def bool_to_string(bool_value):
        if bool_value:
            return 'True'
        else:
            return 'False'

    def coerce(self, value):
        if value is None:
            return self.null()

        try:
            string_value = STRING(value)
        except AWTypeError:
            pass
        else:
            _maybe_bool = self.string_to_bool(string_value)
            if _maybe_bool is not None:
                return _maybe_bool

        try:
            float_value = FLOAT(value)
        except AWTypeError:
            pass
        else:
            return bool(float_value > 0)

        if hasattr(value, '__bool__'):
            try:
                return bool(value)
            except (AttributeError, LookupError, NotImplementedError,
                    TypeError, ValueError):
                self._fail_coercion(value)

        return self.null()

    def normalize(self, value):
        return self.__call__(value)

    def format(self, value, **kwargs):
        value = self.__call__(value)
        return self.bool_to_string(value)


class Integer(BaseType):
    COERCIBLE_TYPES = (bytes, str, float)
    EQUIVALENT_TYPES = (int, )
    NULL = 0

    def coerce(self, value):
        # If casting to int directly fails, try first converting to float,
        # then from float to int. Casting string to int handles "1.5" but
        # "-1.5" fails. The two step approach fixes the negative numbers.
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                float_value = float(value)
            except (ValueError, TypeError):
                pass
            else:
                try:
                    return int(float_value)
                except (ValueError, TypeError):
                    pass

        self._fail_coercion(value)

    def normalize(self, value):
        return self.__call__(value)

    def format(self, value, **kwargs):
        value = self.__call__(value)

        if 'format_string' not in kwargs:
            return '{}'.format(value or self.null())

        format_string = kwargs.get('format_string')
        if format_string:
            if not isinstance(format_string, str):
                raise AWTypeError('Expected "format_string" to be Unicode str')

            try:
                return format_string.format(value)
            except TypeError:
                pass

        raise AWTypeError(
            'Invalid "format_string": "{!s}"'.format(format_string)
        )


class Float(BaseType):
    COERCIBLE_TYPES = (bytes, str, int)
    EQUIVALENT_TYPES = (float, )
    NULL = 0.0

    def coerce(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            self._fail_coercion(value)

    def normalize(self, value):
        return self.__call__(value)

    def bounded(self, value, low=None, high=None):
        _value = self.__call__(value)

        if low is not None:
            low = float(low)
        if high is not None:
            high = float(high)

        if None not in (low, high):
            if low > high:
                raise ValueError('Expected "low" < "high"')

        if low is not None and _value <= low:
            return low
        elif high is not None and _value >= high:
            return high
        else:
            return _value

    def format(self, value, **kwargs):
        value = self.__call__(value)

        if 'format_string' not in kwargs:
            return '{0:.1f}'.format(value or self.null())

        format_string = kwargs.get('format_string')
        if format_string:
            if not isinstance(format_string, str):
                raise AWTypeError('Expected "format_string" to be Unicode str')

            try:
                return format_string.format(value)
            except TypeError:
                pass

        raise AWTypeError(
            'Invalid "format_string": "{!s}"'.format(format_string)
        )


class String(BaseType):
    COERCIBLE_TYPES = (str, bytes, int, float, bool)
    EQUIVALENT_TYPES = (str, )
    NULL = ''

    def coerce(self, value):
        if value is None:
            return self.null()

        if isinstance(value, bytes):
            try:
                return encoding.decode_(value)
            except Exception:
                return self.null()

        if self.acquiescent(value):
            try:
                return str(value)
            except (ValueError, TypeError):
                self._fail_coercion(value)

    def normalize(self, value):
        return self.__call__(value).strip()

    def format(self, value, **kwargs):
        value = self.__call__(value)
        return value


def try_coerce(value):
    coercer = coercer_for(value)
    if coercer:
        try:
            return coercer(value)
        except AWTypeError:
            pass
    return None


def coercer_for(value):
    if value is None:
        return None
    return PRIMITIVE_CUSTOMTYPE_MAP.get(type(value), None)


def force_string(raw_value):
    try:
        str_value = STRING(raw_value)
    except AWTypeError:
        return STRING.null()
    else:
        return str_value


def force_integer(raw_value):
    try:
        int_value = INTEGER(raw_value)
    except AWTypeError:
        return INTEGER.null()
    else:
        return int_value


# Singletons for actual use.
BOOLEAN = Boolean()
PATH = Path()
PATHCOMPONENT = PathComponent()
INTEGER = Integer()
FLOAT = Float()
STRING = String()


# NOTE: Wrapping paths (potentially bytes) with this automatic type
#       detection would coerce them to Unicode strings when we actually
#       want to do path coercion with one the custom types ..
PRIMITIVE_CUSTOMTYPE_MAP = {
    bool: BOOLEAN,
    int: INTEGER,
    float: FLOAT,
    str: STRING,
    bytes: STRING
}
