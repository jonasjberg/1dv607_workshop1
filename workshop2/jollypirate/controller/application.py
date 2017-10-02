# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import logging
import sys

from jollypirate import constants
from .boat import BoatController
from .member import MemberController
from .event import Events


log = logging.getLogger(__name__)


class ApplicationController(object):
    def __init__(self, view):
        self._view = None

        self.view = view

        self.event_handlers = {
            Events.APP_QUIT: self.quit,
            Events.BOAT_DELETE: BoatController.delete,
            Events.BOAT_REGISTER: BoatController.register,
            Events.BOAT_UPDATE: BoatController.update,
            Events.MEMBER_DELETE: MemberController.delete,
            Events.MEMBER_INFOQUERY: MemberController.get_info,
            Events.MEMBER_REGISTER: MemberController.register,
            Events.MEMBER_UPDATE: MemberController.update,
            Events.MEMBERS_LIST: MemberController.list_all,
        }

    def run(self):
        while True:
            choice = self.view.get_selection_from(self.event_handlers.keys())
            log.debug('User entered "{!s}"'.format(choice))

            event_func = None
            for event, handler in self.event_handlers.items():
                if event == choice:
                    event_func = self.event_handlers.get(event)
                    break

            if not event_func:
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
