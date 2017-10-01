# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


# class BaseController(object):
#     def __init__(self, *args, **kwargs):
#         self._views = None
#         self._controllers = None
#
#         _view = kwargs.get('view')
#         if _view:
#             if not isinstance(_view, list):
#                 view = [_view]
#
#         self.view = view
#         self.controller = controller
#
#         if not isinstance(controller, list):
#             controller = [controller]
#
#         for c in controller:
#             self._controller.append(c)
#
#     @property
#     def controller(self):
#         return self._controller
#
#     @controller.setter
#     def controller(self, new_controller):
#         self._controller = new_controller
#
#     @property
#     def view(self):
#         return self._view
#
#     @view.setter
#     def view(self, new_view):
#         self._view = new_view
