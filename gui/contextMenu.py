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
import gui.builtinContextMenus

class ContextMenu(object):
    menus = []
    @classmethod
    def register(cls):
        ContextMenu.menus.append(cls)

    @classmethod
    def getMenu(cls, selection, *fullContexts):
        menu = wx.Menu()
        menu.info = {}
        menu.selection = selection
        empty = True
        menu.Bind(wx.EVT_MENU, cls.handler)
        # Reorder list of contexts
        fullContexts = set(fullContexts)
        orderedFullContexts = []
        for srcContext in gui.builtinContextMenus.srcContextOrder:
            # Compose list of matches against scrContext in provided list of full contexts
            filtered = filter(lambda item: item[0] == srcContext, fullContexts)
            # Append them to reordered list and remove from source
            for match in filtered:
                orderedFullContexts.append(match)
                fullContexts.discard(match)
        # Combine both lists
        orderedFullContexts += fullContexts
        for i, fullContext in enumerate(orderedFullContexts):
            amount = 0
            srcContext = fullContext[0]
            try:
                itmContext = fullContext[1]
            except IndexError:
                itmContext = None
            for menuHandler in cls.menus:
                m = menuHandler()
                if m.display(srcContext, selection):
                    amount += 1
                    texts = m.getText(itmContext, selection)
                    if isinstance(texts, basestring):
                        texts = (texts,)

                    bitmap = m.getBitmap(srcContext, selection)
                    multiple = not isinstance(bitmap, wx.Bitmap)
                    for it, text in enumerate(texts):
                        id = wx.NewId()
                        item = wx.MenuItem(menu, id, text)
                        menu.info[id] = (m, fullContext, it)

                        sub = m.getSubMenu(srcContext, selection, menu, it)
                        if sub is not None:
                            item.SetSubMenu(sub)

                        if bitmap is not None:
                            if multiple:
                                bp = bitmap[it]
                                if bp:
                                    item.SetBitmap(bp)
                            else:
                                item.SetBitmap(bitmap)

                        menu.AppendItem(item)

                    empty = False

            if amount > 0 and i != len(orderedFullContexts) - 1:
                menu.AppendSeparator()

        return menu if empty is False else None

    @classmethod
    def handler(cls, event):
        menu = event.EventObject
        stuff = menu.info.get(event.Id)
        if stuff is not None:
            m, context, i = stuff
            selection = menu.selection
            if not hasattr(selection, "__iter__"):
                selection = (selection,)

            m.activate(context, selection, i)
        else:
            event.Skip()

    def display(self, context, selection):
        raise NotImplementedError()

    def activate(self, context, selection, i):
        return None

    def getSubMenu(self, context, selection, menu, i):
        return None

    def getText(self, context, selection):
        raise NotImplementedError()

    def getBitmap(self, context, selection):
        return None


from gui.builtinContextMenus import *
