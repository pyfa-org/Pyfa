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
import wx.lib.newevent
import controller
import gui.mainFrame
import gui.builtinViewColumns.display as d
import sys
from eos.types import Slot

FitChanged, FIT_CHANGED = wx.lib.newevent.NewEvent()

class FittingView(d.Display):
    DEFAULT_COLS = ["Module state",
                    "Module name/slot",
                    "attr:power",
                    "attr:cpu",
                    "attr:capacitorNeed",
                    "attr:trackingSpeed",
                    "Max range"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Hide() #Don't show ourselves at start
        self.activeFitID = None

    #Gets called from the fitMultiSwitch when it decides its time
    def changeFit(self, fitID):
        self.activeFitID = fitID
        if fitID == None:
            self.Hide()
        else:
            self.Show()

        wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))

    def appendItem(self, itemID):
        fitID = self.activeFitID
        if fitID != None:
            cFit = controller.Fit.getInstance()
            cFit.appendItem(fitID, itemID)
            wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            cFit = controller.Fit.getInstance()
            cFit.removeItem(self.activeFitID, self.mods[self.GetItemData(row)].position)

        wx.PostEvent(self.mainFrame, FitChanged(fitID=self.activeFitID))

    def fitChanged(self, event):
        self.Hide()
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        selection = []
        sel = self.GetFirstSelected()
        while sel != -1:
            selection.append(sel)
            sel = self.GetNextSelected(sel)

        self.DeleteAllItems()
        self.clearItemImages()

        slotOrder = [Slot.SUBSYSTEM, Slot.HIGH, Slot.MED, Slot.LOW, Slot.RIG]

        self.mods = fit.modules[:]
        self.mods.sort(key=lambda mod: (slotOrder.index(mod.slot), mod.position))

        if fit is not None:
            for modid, mod in enumerate(self.mods):
                index = self.InsertStringItem(sys.maxint, "")
                for i, col in enumerate(self.activeColumns):
                    self.SetStringItem(index, i, col.getText(mod), col.getImageId(mod))
                    self.SetItemData(index, modid)


        for i, col in enumerate(self.activeColumns):
            if not col.resized:
                self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
                if self.GetColumnWidth(i) < 40:
                    self.SetColumnWidth(i, 40)

        for sel in selection:
            self.Select(sel)

        self.Show()
        event.Skip()
