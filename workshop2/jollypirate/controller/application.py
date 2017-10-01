# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from collections import namedtuple
import logging
import sys

from jollypirate import constants
from .boat import BoatController
from .member import MemberController
from .event import Events


log = logging.getLogger(__name__)


MenuItem = namedtuple('MenuItem', ['key', 'description'])


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
            Events.BOAT_DELETE: BoatController.delete,
            # Events.BOAT_REGISTER: BoatController.register,
            # Events.BOAT_UPDATE: BoatController.update,
            # Events.MEMBER_DELETE: MemberController.delete,
            # Events.MEMBER_INFOQUERY: MemberController.get_info,
            # Events.MEMBER_REGISTER: MemberController.register,
            # Events.MEMBER_UPDATE: MemberController.update,
            # Events.MEMBERS_LIST: MemberController.list_all,
        }

        self.menu_choices = {
            Events.APP_QUIT: MenuItem(
                key='q', description='Exit Program'
            ),
            Events.BOAT_DELETE: MenuItem(
                key='t', description='Delete a Boat'
            ),
            Events.BOAT_REGISTER: MenuItem(
                key='g', description='Register a Boat'
            ),
            Events.BOAT_UPDATE: MenuItem(
                key='b', description='Update a Boat'
            ),
            Events.MEMBER_DELETE: MenuItem(
                key='u', description='Delete a Member'
            ),
            Events.MEMBER_INFOQUERY: MenuItem(
                key='j', description='Get Information on a Specific Member'
            ),
            Events.MEMBER_REGISTER: MenuItem(
                key='m', description='Register a Member'
            ),
            Events.MEMBER_UPDATE: MenuItem(
                key='k', description='Update a Member'
            ),
            Events.MEMBERS_LIST: MenuItem(
                key='l', description='List all Members'
            ),
        }

    def run(self):
        while True:
            choice = self.view.get_selection_from(self.menu_choices)
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
