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
import gui.fittingView as fv
import gui.marketBrowser as mb
import gui.display as d
from gui.builtinViewColumns.droneCheckbox import DroneCheckbox
from gui.contextMenu import ContextMenu

class DroneView(d.Display):
    DEFAULT_COLS = ["Drone Checkbox",
                    "Drone Name/Amount",
                    "Drone DPS",
                    "Max range",
                    "attr:trackingSpeed",
                    "attr:maxVelocity",]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(mb.ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        if "__WXGTK__" in  wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

    DRONE_ORDER = ('Light Scout Drones', 'Medium Scout Drones',
                   'Heavy Attack Drones', 'Sentry Drones', 'Fighters',
                   'Fighter Bombers', 'Combat Utility Drones',
                   'Electronic Warfare Drones', 'Logistic Drones', 'Mining Drones')
    def droneKey(self, drone):
        item = drone.item
        if item.marketGroup is None:
            item = item.metaGroup.parent

        return (self.DRONE_ORDER.index(item.marketGroup.name),
                drone.item.name)

    def fitChanged(self, event):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(event.fitID)

        self.original = fit.drones if fit is not None else None
        self.drones = stuff = fit.drones[:] if fit is not None else None
        if stuff is not None:
            stuff.sort(key=self.droneKey)

        self.update(stuff)
        event.Skip()


    def addItem(self, event):
        cFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        trigger = cFit.addDrone(fitID, event.itemID)
        if trigger:
            wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
            self.mainFrame.additionsPane.select("Drones")

        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(DroneCheckbox):
                fitID = self.mainFrame.getActiveFit()
                cFit = service.Fit.getInstance()
                drone = self.drones[self.GetItemData(row)]
                cFit.removeDrone(fitID, self.original.index(drone))
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(DroneCheckbox):
                fitID = self.mainFrame.getActiveFit()
                cFit = service.Fit.getInstance()
                drone = self.drones[row]
                cFit.toggleDrone(fitID, self.original.index(drone))
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(DroneCheckbox):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        sel = self.GetFirstSelected()
        if sel != -1:
            cFit = service.Fit.getInstance()
            fit = cFit.getFit(self.mainFrame.getActiveFit())

            menu = ContextMenu.getMenu((fit.drones[sel],), "drone")
            self.PopupMenu(menu)
