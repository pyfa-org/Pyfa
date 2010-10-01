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
import service
import gui.display as d
import gui.fittingView as fv
import gui.marketBrowser as mb

class BoosterView(d.Display):
    DEFAULT_COLS = ["Name",
                    "attr:boosterness"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(mb.ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)

    def fitChanged(self, event):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(event.fitID)

        stuff = fit.boosters if fit is not None else None
        self.populate(stuff)
        self.refresh(stuff)
        event.Skip()

    def addItem(self, event):
        cFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        trigger = cFit.addBooster(fitID, event.itemID)
        if trigger:
            wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))

        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            fitID = self.mainFrame.getActiveFit()
            cFit = service.Fit.getInstance()
            cFit.removeBooster(fitID, self.GetItemData(row))
            wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
