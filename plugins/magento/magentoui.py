# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2012 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

"""Magento UI"""

import gtk

from stoqlib.database.runtime import get_connection
from stoqlib.gui.base.dialogs import run_dialog
from stoqlib.gui.events import StartApplicationEvent, StopApplicationEvent
from stoqlib.lib.translation import stoqlib_gettext

from gui.search.magentosearch import MagentoConfigSearch

_ = stoqlib_gettext


class MagentoUI(object):
    """UI object for magento"""

    def __init__(self):
        self._ui = None
        StartApplicationEvent.connect(self._on_StartApplicationEvent)
        StopApplicationEvent.connect(self._on_StopApplicationEvent)

    #
    #  Private
    #

    def _add_admin_menus(self, uimanager):
        ui_string = """<ui>
          <menubar name="menubar">
            <menu action="SearchMenu">
            <placeholder name="SearchMenuPH">
              <menuitem action="MagentoConfigSearch"/>
            </placeholder>
            </menu>
          </menubar>
        </ui>"""

        ag = gtk.ActionGroup('MagentoMenuActions')
        ag.add_actions([
            ('MagentoConfigSearch', None, _('Magento configs...'),
             None, None, self._on_MagentoConfigSearch__activate),
            ])
        uimanager.insert_action_group(ag, 0)
        self._ui = uimanager.add_ui_from_string(ui_string)

    def _remove_app_ui(self, uimanager):
        if not self._ui:
            return
        uimanager.remove_ui(self._ui)
        self._ui = None

    #
    #  Callbacks
    #

    def _on_MagentoConfigSearch__activate(self, action):
        run_dialog(MagentoConfigSearch, None, get_connection())

    def _on_StartApplicationEvent(self, appname, app):
        if appname == 'admin':
            self._add_admin_menus(app.main_window.uimanager)

    def _on_StopApplicationEvent(self, appname, app):
        self._remove_app_ui(app.main_window.uimanager)
