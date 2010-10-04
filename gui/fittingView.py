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
import service
import gui.mainFrame
import gui.display as d
from gui.contextMenu import ContextMenu
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
                    "Max range",
                    "Module Ammo"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)
        self.activeFitID = None

    #Gets called from the fitMultiSwitch when it decides its time
    def changeFit(self, fitID):
        self.activeFitID = fitID
        self.Show(fitID is not None)
        self.slotsChanged()
        wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))

    def appendItem(self, itemID):
        fitID = self.activeFitID
        if fitID != None:
            cFit = service.Fit.getInstance()
            if cFit.isAmmo(itemID):
                modules = []
                sel = self.GetFirstSelected()
                while sel != -1:
                    modules.append(self.mods[self.GetItemData(sel)].position)
                    sel = self.GetNextSelected(sel)

                cFit.setAmmo(fitID, itemID, modules)
                wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))
            else:
                populate = cFit.appendModule(fitID, itemID)
                if populate:
                    self.slotsChanged()
                if populate is not None:
                    wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            cFit = service.Fit.getInstance()
            populate = cFit.removeModule(self.activeFitID, self.mods[self.GetItemData(row)].position)

            if populate is not None:
                if populate: self.slotsChanged()
                wx.PostEvent(self.mainFrame, FitChanged(fitID=self.activeFitID))

    def generateMods(self):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(self.activeFitID)

        slotOrder = [Slot.SUBSYSTEM, Slot.HIGH, Slot.MED, Slot.LOW, Slot.RIG]

        if fit is not None:
            self.mods = fit.modules[:]
            self.mods.sort(key=lambda mod: (slotOrder.index(mod.slot), mod.position))
        else:
            self.mods = None

    def slotsChanged(self):
        self.generateMods()
        self.populate(self.mods)

    def fitChanged(self, event):
        try:
            if self.activeFitID is not None and self.activeFitID == event.fitID:
                self.generateMods()
                self.refresh(self.mods)

            self.Show(self.activeFitID is not None and self.activeFitID == event.fitID)
        except wx._core.PyDeadObjectError:
            pass
        finally:
            event.Skip()

    def scheduleMenu(self, event):
        event.Skip()
        wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        cFit = service.Fit.getInstance()
        selection = []
        sel = self.GetFirstSelected()
        while sel != -1:
            selection.append(self.mods[self.GetItemData(sel)])
            sel = self.GetNextSelected(sel)

        menu = ContextMenu.getMenu(selection, "module", "ship")
        self.PopupMenu(menu)