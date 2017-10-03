# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import sys

from .base import BaseController
from .. import constants
from .event import Events


class ApplicationController(BaseController):
    def __init__(self, view, member_controller, boat_controller):
        super().__init__(None, view)

        self.view = view
        self._member_controller = member_controller
        self._boat_controller = boat_controller

        self.event_handlers = {
            Events.APP_QUIT: self.quit,
            Events.BOAT_DELETE: self._boat_controller.delete,
            Events.BOAT_REGISTER: self._boat_controller.register,
            # Events.BOAT_UPDATE: self._boat_controller.update,
            Events.MEMBER_DELETE: self._member_controller.delete,
            Events.MEMBER_LIST: self._member_controller.get_info,
            Events.MEMBER_REGISTER: self._member_controller.register,
            Events.MEMBER_MODIFY: self._member_controller.modify,
            Events.MEMBER_LISTALL: self._member_controller.list_all,
        }

    def run(self):
        while True:
            choice = self.view.get_selection_from(self.event_handlers.keys())
            self.log.debug('User entered "{!s}"'.format(choice))

            event_func = None
            for event, handler in self.event_handlers.items():
                if event == choice:
                    event_func = self.event_handlers.get(event)
                    break

            if not event_func or not callable(event_func):
                self.log.warning('Invalid selection: "{!s}"'.format(choice))
            else:
                self.log.debug('Calling event handler "{!s}"'.format(event_func))
                event_func()

    @classmethod
    def quit(cls):
        print('Exiting Application')
        sys.exit(constants.EXIT_SUCCESS)
