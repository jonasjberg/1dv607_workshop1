# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import sys

from .. import (
    exceptions,
    constants
)
from .event import Events
from .base import BaseController


class ApplicationController(BaseController):
    def __init__(self, view, member_controller, boat_controller):
        super().__init__(None, view)

        self.view = view
        self._member_controller = member_controller
        self._boat_controller = boat_controller

        self.event_handlers = {
            Events.APP_QUIT: self.exit_success,
            Events.BOAT_DELETE: self._boat_controller.delete,
            Events.BOAT_REGISTER: self._boat_controller.register,
            Events.BOAT_MODIFY: self._boat_controller.modify,
            Events.MEMBER_DELETE: self._member_controller.delete,
            Events.MEMBER_LIST: self._member_controller.get_info,
            Events.MEMBER_REGISTER: self._member_controller.register,
            Events.MEMBER_MODIFY: self._member_controller.modify,
            Events.MEMBER_LISTALL: self._member_controller.list_all,
        }

    def run(self):
        self.view.msg_application_start()

        try:
            self.infinite_loop()
        except exceptions.JollyPirateException:
            self.exit_failure()
        except KeyboardInterrupt:
            self.exit_success()
        else:
            self.exit_success()

    def infinite_loop(self):
        while True:
            _choices = self.event_handlers.keys()
            choice = self.view.get_main_menu_selection_from(_choices)
            self.log.debug('User entered "{!s}"'.format(choice))

            event_func = None
            for event, handler in self.event_handlers.items():
                if event == choice:
                    event_func = self.event_handlers.get(event)
                    break

            if not event_func or not callable(event_func):
                self.log.warning('Invalid selection: "{!s}"'.format(choice))
            else:
                self.log.debug(
                    'Calling event handler "{!s}"'.format(event_func)
                )
                event_func()

    def exit_success(self):
        self.view.msg_application_success()
        sys.exit(constants.EXIT_SUCCESS)

    def exit_failure(self):
        self.view.msg_application_failure()
        sys.exit(constants.EXIT_SUCCESS)

