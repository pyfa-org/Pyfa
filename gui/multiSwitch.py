# =============================================================================
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
# =============================================================================

from gui.chrome_tabs import ChromeNotebook
import gui.builtinViews.emptyView


class MultiSwitch(ChromeNotebook):
    def __init__(self, parent):
        ChromeNotebook.__init__(self, parent)
        # self.AddPage() # now handled by mainFrame
        self.handlers = handlers = []
        for type in TabSpawner.tabTypes:
            handlers.append(type(self))

    def handleDrag(self, type, info):
        for handler in self.handlers:
            h = getattr(handler, "handleDrag", None)
            if h:
                h(type, info)

    def AddPage(self, tabWnd=None, tabTitle="Empty Tab", tabImage=None):
        if tabWnd is None:
            tabWnd = gui.builtinViews.emptyView.BlankPage(self)
            tabWnd.handleDrag = lambda type, info: self.handleDrag(type, info)

        ChromeNotebook.AddPage(self, tabWnd, tabTitle, tabImage, True)

    def DeletePage(self, n, *args, **kwargs):
        ChromeNotebook.DeletePage(self, n, *args, **kwargs)
        if self.GetPageCount() == 0:
            self.AddPage()


class TabSpawner(object):
    tabTypes = []

    @classmethod
    def register(cls):
        TabSpawner.tabTypes.append(cls)
