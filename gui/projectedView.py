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
import gui.display as d
import gui.fittingView as fv
import service
import gui.droneView
from gui.builtinViewColumns.projectedState import ProjectedState
from gui.contextMenu import ContextMenu
import eos.types

class ProjectedView(d.Display):
    DEFAULT_COLS = ["Projected Ammo Icon",
                    "Projected State",
                    "Projected Name",
                    "Projected Ammo"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(fv.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.remove)
        self.droneView = gui.droneView.DroneView

    def moduleSort(self, module):
        return module.item.name

    def droneSort(self, drone):
        item = drone.item
        if item.marketGroup is None:
            item = item.metaGroup.parent

        return (self.droneView.DRONE_ORDER.index(item.marketGroup.name),
                drone.item.name)

    def fitSort(self, fit):
        return fit.name

    def fitChanged(self, event):
        cFit = service.Fit.getInstance()
        fit = cFit.getFit(event.fitID)
        stuff = []
        if fit is not None:
            self.modules = fit.projectedModules[:]
            self.drones = fit.projectedDrones[:]
            self.fits = fit.projectedFits[:]

            self.modules.sort(key=self.moduleSort)
            self.drones.sort(key=self.droneSort)
            self.fits.sort(key=self.fitSort)

            stuff.extend(self.modules)
            stuff.extend(self.drones)
            stuff.extend(self.fits)

        self.update(stuff)

    def get(self, row):
        numMods = len(self.modules)
        numDrones = len(self.drones)
        if row < numMods:
            stuff = self.modules[row]
        elif row - numMods < numDrones:
            stuff = self.drones[row - numMods]
        else:
            stuff = self.fits[row - numMods - numDrones]

        return stuff

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            item = self.get(row)
            col = self.getColumn(event.Position)
            if col == self.getColIndex(ProjectedState):
                fitID = self.mainFrame.getActiveFit()
                cFit = service.Fit.getInstance()
                cFit.toggleProjected(fitID, item, "right" if event.Button == 3 else "left")
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
            elif event.Button == 3:
                if isinstance(item, eos.types.Drone):
                    context = ("projectedDrone",)
                elif isinstance(item, eos.types.Module):
                    if item.charge is not None:
                        context = ("projectedModule", "projectedAmmo")
                    else:
                        context = ("projectedModule",)
                else:
                    context = ("projectedFit",)

                print context
                menu = ContextMenu.getMenu((item,), *context)
                print menu
                self.PopupMenu(menu)

    def remove(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(ProjectedState):
                fitID = self.mainFrame.getActiveFit()
                cFit = service.Fit.getInstance()
                cFit.removeProjected(fitID, self.get(row))
                wx.PostEvent(self.mainFrame, fv.FitChanged(fitID=fitID))
