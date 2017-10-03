# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from . import (
    controller,
    model,
    view
)


def initialize_application():
    app_view = view.ApplicationView()
    member_view = view.MemberView()
    boat_view = view.BoatView()

    member_model = model.MemberModel()
    boat_model = model.BoatModel()

    member_controller = controller.MemberController(member_model, member_view)
    boat_controller = controller.BoatController(boat_model, boat_view)
    app_controller = controller.ApplicationController(
        app_view, member_controller, boat_controller
    )
    return app_controller


def application():
    return initialize_application()

