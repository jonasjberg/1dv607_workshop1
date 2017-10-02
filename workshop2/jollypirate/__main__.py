# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

from jollypirate import jollypirate
from .jollypirate import constants

log = logging.getLogger(__name__)


def main(args):
    try:
        app = jollypirate.application()
        app.run()
    except KeyboardInterrupt:
        sys.exit(constants.EXIT_FAILURE)
    else:
        sys.exit(constants.EXIT_SUCCESS)


if __name__ == '__main__':
    main(sys.argv)
