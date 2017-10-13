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

from .. import (
    constants,
    exceptions,
    util
)
from ..util import encoding as enc
from ..util import types


# Absolute path to persistent storage.
JOLLYPIRATE_APPDATA_ABSPATH = enc.normpath(
    os.path.realpath(os.path.join(constants.PROJECT_ROOT_ABSPATH,
                                  'appdata'))
)


DATA_STORAGE_ABSPATH = enc.normpath(JOLLYPIRATE_APPDATA_ABSPATH)
assert DATA_STORAGE_ABSPATH not in ('', None)


log = logging.getLogger(__name__)


class BaseStorage(object):
    """
    Abstract base class for all file-based storage implementations.

    Example initialization and storage:

        c = BaseStorage('mystorage')
        c.set('mydata', {'a': 1, 'b': 2})

    This will storage the data in memory by storing in a class instance dict,
    and also write the data to disk using the path:

        "STORAGE_DIR_ABSPATH/mystorage_mydata"

    Example retrieval:

        stored_data = c.get('mydata')
        assert stored_data == {'a': 1, 'b': 2}

    The idea is to keep many smaller files instead of a single shared file
    for possibly easier pruning of old date, file size limits, etc.

    Inheriting class must implement '_load' and '_dump' which does the actual
    serialization and reading/writing to disk.
    """
    STORAGEFILE_PREFIX_SEPARATOR = '_'

    def __init__(self, storagefile_prefix):
        self._data = dict()

        _prefix = types.force_string(storagefile_prefix)
        if not _prefix.strip():
            raise ValueError(
                'Argument "storagefile_prefix" must be a valid string'
            )
        self.storagefile_prefix = _prefix

        self._dp = enc.displayable_path(JOLLYPIRATE_APPDATA_ABSPATH)

        if not self.has_storagedir():
            log.debug('Storage directory does not exist: "{!s}"'.format(self._dp))

            try:
                util.makedirs(JOLLYPIRATE_APPDATA_ABSPATH)
            except exceptions.FilesystemError as e:
                raise exceptions.DataPersistenceError(
                    'Unable to create storage directory "{!s}";'
                    ' {!s}'.format(self._dp, e)
                )
            else:
                log.info('Created storage directory: "{!s}"'.format(self._dp))

        if not self.has_storagedir_permissions():
            raise exceptions.DataPersistenceError(
                'Storage path requires RWX-permissions: "{!s}'.format(self._dp)
            )
        log.debug('{!s} Using storage path "{!s}'.format(self, self._dp))

    @staticmethod
    def has_storagedir_permissions():
        try:
            return util.has_permissions(JOLLYPIRATE_APPDATA_ABSPATH, 'rwx')
        except (TypeError, ValueError):
            return False

    @staticmethod
    def has_storagedir():
        _path = enc.syspath(JOLLYPIRATE_APPDATA_ABSPATH)
        try:
            return bool(os.path.exists(_path) and os.path.isdir(_path))
        except (OSError, ValueError, TypeError):
            return False

    def _storage_file_abspath(self, key):
        string_key = types.force_string(key)
        if not string_key.strip():
            raise KeyError('Invalid key: "{!s}" ({!s})'.format(key, type(key)))

        _basename = '{pre}{sep}{key}'.format(
            pre=self.storagefile_prefix,
            sep=self.STORAGEFILE_PREFIX_SEPARATOR,
            key=key
        )
        _p = enc.normpath(
            os.path.join(enc.syspath(DATA_STORAGE_ABSPATH),
                         enc.syspath(enc.encode_(_basename)))
        )
        return _p

    def get(self, key):
        """
        Returns data from the persistent data store.

        Args:
            key (str): The key of the data to retrieve.
                       Postfix of the storage file that is written to disk.

        Returns:
            Any stored data stored with the given key, as any serializable type.
        Raises:
            KeyError: The given 'key' is not a valid non-empty string,
                      or the key is not found in the persistent data.
            DataPersistenceError: Failed to read persistent data due to data
                                  corruption, encoding errors, missing files, ..
        """
        if not key:
            raise KeyError

        if key not in self._data:
            _file_path = self._storage_file_abspath(key)
            if not os.path.exists(enc.syspath(_file_path)):
                # Avoid displaying errors on first use.
                raise KeyError

            try:
                value = self._load(_file_path)
                self._data[key] = value
            except ValueError as e:
                _dp = enc.displayable_path(_file_path)
                log.error(
                    'Error when reading key "{!s}" from storage file "{!s}" '
                    '(corrupt file?); {!s}'.format(key, _dp, e)
                )
                self.delete(key)
            except OSError as e:
                _dp = enc.displayable_path(_file_path)
                log.debug(
                    'Error while trying to read key "{!s}" from storage file '
                    '"{!s}"; {!s}'.format(key, _dp, e)
                )
                raise KeyError
            except Exception as e:
                raise exceptions.DataPersistenceError(
                    'Error while reading storage; {!s}'.format(e)
                )

        return self._data.get(key)

    def set(self, key, value):
        """
        Stores data in the persistent data store.

        Args:
            key (str): The key to store the data under.
                       Postfix of the storage file that is written to disk.
            value: The data to store, as any serializable type.
        """
        self._data[key] = value

        _file_path = self._storage_file_abspath(key)
        try:
            self._dump(value, _file_path)
        except OSError as e:
            _dp = enc.displayable_path(_file_path)
            log.error(
                'Error while trying to write key "{!s}" with value "{!s}" to '
                'storage file "{!s}"; {!s}'.format(key, value, _dp, e)
            )
        else:
            _dp = enc.displayable_path(_file_path)
            log.debug(
                'Wrote key "{!s}" with value "{!s}" to '
                'storage file "{!s}"'.format(key, value, _dp)
            )

    def delete(self, key):
        try:
            del self._data[key]
        except KeyError:
            pass

        _p = self._storage_file_abspath(key)
        _dp = enc.displayable_path(_p)
        log.debug('Deleting file "{!s}"'.format(_dp))
        try:
            util.delete(_p, ignore_missing=True)
        except OSError as e:
            raise exceptions.DataPersistenceError(
                'Error when trying to delete "{!s}"; {!s}'.format(_dp, e)
            )

    def has(self, key):
        # TODO: [TD0097] Test this ..
        if key in self._data:
            return True

        _file_path = self._storage_file_abspath(key)
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
