# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import os

from jollypirate import constants
from .implementation import PickleStorage


def get_implementation(cachefile_prefix):
    return PickleStorage(cachefile_prefix)
