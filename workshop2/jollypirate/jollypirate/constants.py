# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import os


EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEFAULT_DATETIME_FORMAT_DATETIME = '%Y-%m-%dT%H%M%S'
DEFAULT_DATETIME_FORMAT_DATE = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT_TIME = '%H-%M-%S'

# Absolute path to the parent directory of this file.
_abspath_self_dir = os.path.realpath(os.path.dirname(__file__))

# Absolute path to '..' relative from the path of this file.
PROJECT_ROOT_ABSPATH = os.path.normpath(os.path.realpath(
    os.path.join(_abspath_self_dir, os.path.pardir))
)
# assert os.path.isdir(PROJECT_ROOT_ABSPATH)
# assert os.path.isabs(PROJECT_ROOT_ABSPATH)

