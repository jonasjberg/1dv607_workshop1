# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class BaseController(object):
    def __init__(self, model, view):
        self._model = None
        self._view = None

        self.model = model
        self.view = view

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, new_model):
        self._model = new_model

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, new_view):
        self._view = new_view
