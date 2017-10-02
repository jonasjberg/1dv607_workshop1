# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import os

from jollypirate import constants


# Absolute path to persistent storage.
JOLLYPIRATE_APPDATA_ABSPATH = os.path.normpath(
    os.path.realpath(os.path.join(constants.PROJECT_ROOT_ABSPATH,
                                  'appdata'))
)


