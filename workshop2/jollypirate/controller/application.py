# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

from jollypirate import constants
from .event import (
    # BoatController,
    Events,
    # MemberController
)


log = logging.getLogger(__name__)


class ApplicationController(object):
    def __init__(self, view, controller=None):
        self._view = None
        self._controller = []

        self.view = view
        # self.controller = controller

        # if not isinstance(controller, list):
        #     controller = [controller]

        # for c in controller:
        #     self._controller.append(c)

        self.event_handlers = {
            Events.APP_QUIT: self.quit,
            # EVENTS.BOAT_DELETE: BoatController.delete
            # EVENTS.BOAT_REGISTER: BoatController.register,
            # EVENTS.BOAT_UPDATE: BoatController.update,
            # EVENTS.MEMBER_DELETE: MemberController.delete,
            # EVENTS.MEMBER_INFOQUERY: MemberController.get_info,
            # EVENTS.MEMBER_REGISTER: MemberController.register,
            # EVENTS.MEMBER_UPDATE: MemberController.update,
            # EVENTS.MEMBERS_LIST: MemberController.list_all,
        }

    def run(self):
        while True:
            choice = self.view.get_userinput('TODO: choices ..')
            log.debug('User entered "{!s}"'.format(choice))

            func = self.event_handlers.get(choice)
            if not func:
                log.warning('Invalid selection: "{!s}"'.format(choice))
            else:
                func()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, new_controller):
        self._controller = new_controller

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, new_view):
        self._view = new_view

    @classmethod
    def quit(cls):
        log.info('Exiting!')
        sys.exit(constants.EXIT_SUCCESS)
