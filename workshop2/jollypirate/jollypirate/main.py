# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .view.application import ApplicationView
from .view.member import MemberView
from .view.boat import BoatView

from jollypirate.jollypirate.controller import *


def initialize_application():
    app_view = ApplicationView()
    member_view = MemberView()
    boat_view = BoatView()

    member_controller = MemberController(member_view)
    boat_controller = BoatController(boat_view)
    app_controller = ApplicationController(app_view,
                                           member_controller,
                                           boat_controller)
    return app_controller


def application():
    return initialize_application()
