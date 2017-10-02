# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

from .. import constants
from .boat import BoatController
from .event import Events
from .member import MemberController
from ..model import MemberRegistry

log = logging.getLogger(__name__)


class ApplicationController(object):
    def __init__(self, view, member_controller, boat_controller):
        self._view = None

        self.view = view
        self._member_controller = member_controller
        self._boat_controller = boat_controller

        self.event_handlers = {
            Events.APP_QUIT: self.quit,
            # Events.BOAT_DELETE: BoatController.delete,
            # Events.BOAT_REGISTER: BoatController.register,
            # Events.BOAT_UPDATE: BoatController.update,
            # Events.MEMBER_DELETE: MemberController.delete,
            Events.MEMBER_LIST: self._member_controller.get_info,
            # Events.MEMBER_REGISTER: MemberController.register,
            # Events.MEMBER_UPDATE: MemberController.update,
            Events.MEMBER_LISTALL: self._member_controller.list_all,
        }

        # self._member_registry = MemberRegistry.fromfile(
        #     constants.PERSISTANCE_MEMBERREGISTRY_PATH
        # )

    def run(self):
        while True:
            choice = self.view.get_selection_from(self.event_handlers.keys())
            log.debug('User entered "{!s}"'.format(choice))

            event_func = None
            for event, handler in self.event_handlers.items():
                if event == choice:
                    event_func = self.event_handlers.get(event)
                    break

            if not event_func or not callable(event_func):
                log.warning('Invalid selection: "{!s}"'.format(choice))
            else:
                log.debug('Calling event handler "{!s}"'.format(event_func))
                event_func()

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
