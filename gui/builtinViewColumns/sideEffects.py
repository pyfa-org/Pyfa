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


# noinspection PyPackageRequirements
import wx
from eos.saveddata.booster import Booster
from gui.viewColumn import ViewColumn
import gui.mainFrame


class SideEffects(ViewColumn):
    name = "Side Effects"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.columnText = "Active Side Effects"
        self.mask = wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if isinstance(stuff, Booster):
            active = [x.name for x in stuff.sideEffects if x.active]
            if len(active) == 0:
                return "None"
            return ", ".join(active)


SideEffects.register()
