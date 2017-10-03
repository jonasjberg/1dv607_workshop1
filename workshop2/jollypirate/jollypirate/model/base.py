# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging


class BaseModel(object):
    def __init__(self):
        self.log = logging.getLogger(str(self))

    def __str__(self):
        return self.__class__.__name__

    def __getstate__(self):
        # Exclude the 'logging' instance when serializing the object.
        return {k: v for k, v in self.__dict__.items() if k != 'log'}
