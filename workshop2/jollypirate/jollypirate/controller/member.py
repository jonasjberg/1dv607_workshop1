# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

from .. import exceptions
from ..model import MemberModel
from .base import BaseController


class MemberController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)

    def delete(self):
        self.view.msg_member_deletion_start()

        _members = self.member_registry.getall()
        _menu_items = self._members_as_menu_items(_members)
        _should_delete = self.view.get_selection_from(_menu_items)
        if _should_delete:
            try:
                self.member_registry.remove(_should_delete)
            except exceptions.JollyPirateModelError as e:
                self.view.display_msg_failure(str(e))
                self.view.msg_member_deletion_failure()
            else:
                self.view.msg_member_deletion_success()

    def get_info(self):
        self.view.msg_member_info_start()

        _members = self.member_registry.getall()
        _menu_items = self._members_as_menu_items(_members)
        _get_info_on = self.view.get_selection_from(_menu_items)
        if _get_info_on:
            self.view.display_member_info(_get_info_on)
            self.view.msg_member_info_success()

    def register(self):
        self.view.msg_member_registration_start()

        _new_member = MemberModel()

        # Data validation is handled in the model.
        self.populate_model_data(
            _new_member, model_field='name_first', field_name='First Name'
        )
        self.populate_model_data(
            _new_member, model_field='name_last', field_name='Last Name'
        )
        self.populate_model_data(
            _new_member, model_field='social_sec_number',
            field_name='Social Security Number (YYYYMMDD-XXXX)'
        )

        try:
            self.member_registry.add(_new_member)
        except exceptions.JollyPirateModelError as e:
            self.view.display_error(e)
            self.view.msg_member_registration_failure()
        else:
            self.view.msg_member_registration_success()

    def modify(self):
        self.view.msg_member_modify_start()

        _members = self.member_registry.getall()
        _menu_items = self._members_as_menu_items(_members)
        _should_modify = self.view.get_selection_from(_menu_items)
        if not _should_modify:
            self.view.msg_member_modify_failure()
            return

        _member = MemberModel.copy(_should_modify)
        self.populate_model_data(
            _member, model_field='name_first', field_name='First Name'
        )
        self.populate_model_data(
            _member, model_field='name_last', field_name='Last Name'
        )

        self.populate_model_data(
            _member, model_field='social_sec_number',
            field_name='Social Security Number',
        )

        try:
            self.member_registry.remove(_should_modify)
            self.member_registry.add(_member)
        except exceptions.JollyPirateModelError as e:
            self.view.display_msg_failure(str(e))
            self.view.msg_member_modify_failure()
        else:
            self.view.msg_member_modify_success()

    def list_all(self):
        _members = self.member_registry.getall()
        self.view.list(_members)
