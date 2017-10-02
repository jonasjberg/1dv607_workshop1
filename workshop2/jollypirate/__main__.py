# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

import jollypirate


log = logging.getLogger(__name__)


def main(args):
    try:
        app = jollypirate.application()
        app.run()
    except KeyboardInterrupt:
        # sys.exit(jollypirate.constants.EXIT_FAILURE)
        pass
    else:
        # sys.exit(jollypirate.constants.EXIT_SUCCESS)
        pass


if __name__ == '__main__':
    main(sys.argv)
