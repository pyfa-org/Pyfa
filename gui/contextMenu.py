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
    menus = []
    activeMenu = {}
    @classmethod
    def register(cls):
        ContextMenu.menus.append(cls)

    @classmethod
    def getMenu(cls, selection, *contexts):
        menu = wx.Menu()
        empty = True
        for i, context in enumerate(contexts):
            amount = 0
            for menuHandler in cls.menus:
                m = menuHandler()
                if m.display(context, selection):
                    amount += 1
                    texts = m.getText(context, selection)
                    if isinstance(texts, basestring):
                        texts = (texts,)

                    for it, text in enumerate(texts):
                        id = wx.NewId()
                        item = wx.MenuItem(menu, id, text)
                        cls.activeMenu[id] = (m, context, selection, it)

                    menu.Bind(wx.EVT_MENU, cls.handler)
                    bitmap = m.getBitmap(context, selection)
                    if bitmap:
                        item.SetBitmap(bitmap)

                    menu.AppendItem(item)
                    empty = False

            if amount > 0 and i != len(contexts) - 1:
                menu.AppendSeparator()

        return menu if not empty else None

    @classmethod
    def handler(cls, event):
        m, context, selection, i = cls.activeMenu[event.Id]
        cls.activeMenu.clear()
        m.activate(context, selection, i)

    def display(self, context, selection):
        raise NotImplementedError()

    def activate(self, context, selection, i):
        raise NotImplementedError()

    def getText(self, context, selection):
        raise NotImplementedError()

    def getBitmap(self, context, selection):
        return None

from gui.builtinContextMenus import *
