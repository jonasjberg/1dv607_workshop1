# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

from jollypirate import constants
from jollypirate.controller import *
from jollypirate.view import *


log = logging.getLogger(__name__)


def initialize_application():
    app_view = ApplicationView()
    member_view = MemberView()
    boat_view = BoatView()

    member_controller = MemberController(member_view)
    boat_controller = BoatController(boat_view)
    app_controller = ApplicationController(app_view)

    return app_controller


if __name__ == '__main__':
    try:
        app = initialize_application()
        app.run()
    except KeyboardInterrupt:
        sys.exit(constants.EXIT_FAILURE)
    else:
        sys.exit(constants.EXIT_SUCCESS)

