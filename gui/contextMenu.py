#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx

class ContextMenu(object):
    menus = set()
    @classmethod
    def register(cls):
        cls.menus.add(cls())

    @classmethod
    def getMenu(cls, *contexts):
        menu = wx.Menu()
        for i, m in enumerate(cls.menus):
            amount = 0
            for context in contexts:
                if m.display(context):
                    amount += 1
                    item = wx.MenuItem(menu, wx.ID_ANY, m.getText(context))
                    bitmap = m.getBitmap(context)
                    if bitmap:
                        item.SetBitmap(bitmap)

                    menu.AppendItem(item)

            if amount > 0 and i != len(cls.menus) - 1:
                menu.AppendSeparator()

        return menu

    def display(self, context):
        raise NotImplementedError()

    def activate(self, context):
        raise NotImplementedError()

    def getText(self, context):
        raise NotImplementedError()

    def getBitmap(self, context):
        return None

from gui.builtinContextMenus import *