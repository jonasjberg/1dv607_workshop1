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

import logging
import os

from jollypirate import util
from jollypirate import constants
from jollypirate.exceptions import JollyPirateException
from jollypirate.util import encoding as enc
from jollypirate.util import types


# Absolute path to persistent storage.
JOLLYPIRATE_APPDATA_ABSPATH = os.path.normpath(
    os.path.realpath(os.path.join(constants.PROJECT_ROOT_ABSPATH,
                                  'appdata'))
)


CACHE_DIR_ABSPATH = enc.normpath(JOLLYPIRATE_APPDATA_ABSPATH)
assert CACHE_DIR_ABSPATH not in ('', None)


log = logging.getLogger(__name__)


class DataPersistenceError(JollyPirateException):
    """Irrecoverable error while reading or writing data to disk."""


class BaseStorage(object):
    """
    Abstract base class for all file-based cache implementations.

    Example initialization and storage:

        c = AutonameowCache('mycache')
        c.set('mydata', {'a': 1, 'b': 2})

    This will cache the data in memory by storing in a class instance dict,
    and also write the data to disk using the path:

        "CACHE_DIR_ABSPATH/mycache_mydata"

    Example retrieval:

        cached_data = c.get('mydata')
        assert cached_data == {'a': 1, 'b': 2}

    The idea is to keep many smaller files instead of a single shared file
    for possibly easier pruning of old date, file size limits, etc.

    Inheriting class must implement '_load' and '_dump' which does the actual
    serialization and reading/writing to disk.
    """
    CACHEFILE_PREFIX_SEPARATOR = '_'

    def __init__(self, cachefile_prefix):
        self._data = {}

        _prefix = types.force_string(cachefile_prefix)
        if not _prefix.strip():
            raise ValueError(
                'Argument "cachefile_prefix" must be a valid string'
            )
        self.cachefile_prefix = _prefix

        if not os.path.exists(enc.syspath(CACHE_DIR_ABSPATH)):
            raise DataPersistenceError(
                'Cache directory does not exist: "{!s}"'.format(
                    enc.displayable_path(CACHE_DIR_ABSPATH)
                )
            )

            # TODO: [TD0097] Add proper handling of cache directories.
            # try:
            #     os.makedirs(enc.syspath(self._cache_dir))
            # except OSError as e:
            #     raise CacheError(
            #         'Error while creating cache directory "{!s}": '
            #         '{!s}'.format(enc.displayable_path(self._cache_dir), e)
            #     )
        else:
            if not util.has_permissions(CACHE_DIR_ABSPATH, 'rwx'):
                raise DataPersistenceError(
                    'Cache directory path requires RWX-permissions: '
                    '"{!s}'.format(enc.displayable_path(CACHE_DIR_ABSPATH))
                )
        log.debug('{!s} Using _cache_dir "{!s}'.format(
            self, enc.displayable_path(CACHE_DIR_ABSPATH))
        )

    def _cache_file_abspath(self, key):
        string_key = types.force_string(key)
        if not string_key.strip():
            raise KeyError('Invalid key: "{!s}" ({!s})'.format(key, type(key)))

        _basename = '{pre}{sep}{key}'.format(
            pre=self.cachefile_prefix,
            sep=self.CACHEFILE_PREFIX_SEPARATOR,
            key=key
        )
        _p = enc.normpath(
            os.path.join(enc.syspath(CACHE_DIR_ABSPATH),
                         enc.syspath(enc.encode_(_basename)))
        )
        return _p

    def get(self, key):
        """
        Returns data from the cache.

        Args:
            key (str): The key of the data to retrieve.
                       Postfix of the cache file that is written to disk.

        Returns:
            Any cached data stored with the given key, as any serializable type.
        Raises:
            KeyError: The given 'key' is not a valid non-empty string,
                      or the key is not found in the cached data.
            CacheError: Failed to read cached data for some reason;
                        data corruption, encoding errors, missing files, etc..
        """
        if not key:
            raise KeyError

        if key not in self._data:
            _file_path = self._cache_file_abspath(key)
            _dp = enc.displayable_path(_file_path)
            try:
                value = self._load(_file_path)
                self._data[key] = value
            except ValueError as e:
                log.error(
                    'Error when reading key "{!s}" from cache file "{!s}" '
                    '(corrupt file?); {!s}'.format(key, _dp, e)
                )
                self.delete(key)
            except OSError as e:
                log.warning(
                    'Error while trying to read key "{!s}" from cache file '
                    '"{!s}"; {!s}'.format(key, _dp, e)
                )
                raise KeyError
            except Exception as e:
                raise DataPersistenceError('Error while reading cache; {!s}'.format(e))

        return self._data.get(key)

    def set(self, key, value):
        """
        Stores data in the cache.

        Args:
            key (str): The key to store the data under.
                       Postfix of the cache file that is written to disk.
            value: The data to store, as any serializable type.
        """
        self._data[key] = value

        _file_path = self._cache_file_abspath(key)
        try:
            self._dump(value, _file_path)
        except OSError as e:
            _dp = enc.displayable_path(_file_path)
            log.error(
                'Error while trying to write key "{!s}" with value "{!s}" to '
                'cache file "{!s}"; {!s}'.format(key, value, _dp, e)
            )

    def delete(self, key):
        try:
            del self._data[key]
        except KeyError:
            pass

        _dp = enc.displayable_path(self._cache_file_abspath(key))
        try:
            log.critical('would have deleted "{!s}"'.format(_dp))
            # TODO: [TD0097] Double-check this and actually delete the file ..
            pass
        except OSError as e:
            raise DataPersistenceError(
                'Error when trying to delete "{!s}"; {!s}'.format(_dp, e)
            )

    def has(self, key):
        # TODO: [TD0097] Test this ..
        if key in self._data:
            return True

        _file_path = self._cache_file_abspath(key)
        try:
            os.path.exists(_file_path)
        except OSError:
            return False
        else:
            return True

    def _load(self, file_path):
        raise NotImplementedError('Must be implemented by inheriting classes.')

    def _dump(self, value, file_path):
        raise NotImplementedError('Must be implemented by inheriting classes.')

    def __str__(self):
        return self.__class__.__name__
