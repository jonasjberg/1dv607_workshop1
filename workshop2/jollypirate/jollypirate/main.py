# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from jollypirate.model import MemberModel
from jollypirate.view.application import ApplicationView
from jollypirate.view.member import MemberView
from jollypirate.view.boat import BoatView
from jollypirate.controller import *


def initialize_application():
    app_view = ApplicationView()
    member_view = MemberView()
    boat_view = BoatView()

    member_model = MemberModel()

    member_controller = MemberController(member_model, member_view)
    boat_controller = BoatController(boat_view)
    app_controller = ApplicationController(app_view,
                                           member_controller,
                                           boat_controller)
    return app_controller


def application():
    return initialize_application()

