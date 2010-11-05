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

from gui.viewColumn import ViewColumn
import gui.builtinViewColumns.name
import gui.builtinViewColumns.droneNameAmount
from eos.types import Drone, Fit
import wx
from gui import bitmapLoader

class ProjectedName(ViewColumn):
    name = "Projected Name"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.columnText = "Name"
        self.mask = wx.LIST_MASK_TEXT
        self.shipImage = fittingView.imageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))
        self.slave = gui.builtinViewColumns.name.StuffName(fittingView, params)
        self.droneSlave = gui.builtinViewColumns.droneNameAmount.DroneNameAmount(fittingView, params)

    def getText(self, stuff):
        if isinstance(stuff, Drone):
            return self.droneSlave.getText(stuff)
        elif isinstance(stuff, Fit):
            return "%s (%s)" % (stuff.name, stuff.ship.item.name)
        else:
            return self.slave.getText(stuff)

    def getImageId(self, thing):
        if isinstance(thing, Drone):
            return self.droneSlave.getImageId(thing)
        elif isinstance(thing, Fit):
            return self.shipImage
        else:
            return self.slave.getImageId(thing)

ProjectedName.register()
