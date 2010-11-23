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
import gui.chromeTabs
import gui.mainFrame

class MultiSwitch(gui.chromeTabs.PFNotebook):
    def __init__(self, parent):
        gui.chromeTabs.PFNotebook.__init__(self, parent)
        self.AddPage()
        self.handlers = handlers = []
        for type in TabSpawner.tabTypes:
            handlers.append(type(self))

    def handleDrag(self, type, info, spawnTab=True):
        if spawnTab:
            self.AddPage()

        for handler in self.handlers:
            h = getattr(handler, "handleDrag", None)
            if h:
                h(type, info)

    def AddPage(self, tabWnd=None, tabTitle="Empty Tab",  tabImage=None):
        if tabWnd is None:
            tabWnd = wx.Panel(self, size=(0, 0))
            tabWnd.handleDrag = lambda type, info: self.handleDrag(type, info, False)

        gui.chromeTabs.PFNotebook.AddPage(self, tabWnd, tabTitle, tabImage, True)


    def DeletePage(self, n, *args, **kwargs):
        if self.GetPageCount() > 1:
            gui.chromeTabs.PFNotebook.DeletePage(self, n, *args, **kwargs)
        else:
            gui.mainFrame.MainFrame.getInstance().Close()

class TabSpawner(object):
    tabTypes = []
    @classmethod
    def register(cls):
        TabSpawner.tabTypes.append(cls)
