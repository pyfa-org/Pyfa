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

import controller
import gui.mainFrame
from gui import bitmapLoader
import gui.fittingView as fv
import gui.marketBrowser as mb
import gui.builtinViewColumns.display as d
from gui.builtinViewColumns import registerColumn
from gui.viewColumn import ViewColumn

class DroneView(d.Display):
    DEFAULT_COLS = ["Activate Drone",
                    "Deactivate Drone",
                    "Drone Name/Amount",
                    "Drone DPS",
                    "Max range",
                    "attr:trackingSpeed",
                    "attr:maxVelocity",]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(mb.ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)

    def fitChanged(self, event):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(event.fitID)

        self.populate(fit.drones if fit is not None else None)

    def addItem(self, event):
        cFit = controller.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        cFit.addDrone(fitID, event.itemID)
        wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            fitID = self.mainFrame.getActiveFit()
            cFit = controller.Fit.getInstance()
            cFit.removeDrone(fitID, self.GetItemData(row))

            wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))

class DroneMore(ViewColumn):
    name = "Activate Drone"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        bitmap = bitmapLoader.getBitmap("more_small", "icons")
        self.moreId = fittingView.imageList.Add(bitmap)
        self.size = 16
        self.columnText = ""

    def getText(self, drone):
        return ""

    def getImageId(self, mod):
        return self.moreId

class DroneLess(ViewColumn):
    name = "Deactivate Drone"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        bitmap = bitmapLoader.getBitmap("less_small", "icons")
        self.lessId = fittingView.imageList.Add(bitmap)
        self.size = 16
        self.columnText = ""

    def getText(self, drone):
        return ""

    def getImageId(self, mod):
        return self.lessId

registerColumn(DroneMore)
registerColumn(DroneLess)
