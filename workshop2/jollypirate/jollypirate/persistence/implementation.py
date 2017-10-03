# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

try:
    import cPickle as pickle
except ImportError:
    import pickle

from ..persistence.abstract import BaseStorage
from ..util import encoding as enc


class PickleStorage(BaseStorage):
    """
    Implementation using a very simple standard library serialization module.
    """
    def _load(self, file_path):
        with open(enc.syspath(file_path), 'rb') as fh:
            return pickle.load(fh, encoding='bytes')

    def _dump(self, value, file_path):
        with open(enc.syspath(file_path), 'wb') as fh:
            pickle.dump(value, fh, pickle.HIGHEST_PROTOCOL)
