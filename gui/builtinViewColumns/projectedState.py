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

from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
from gui import bitmapLoader
from eos.types import Slot
import gui.builtinViewColumns.moduleState
import gui.builtinViewColumns.droneCheckbox
from eos.types import Module, Drone, Fit
import gui.bitmapLoader

class ProjectedState(ViewColumn):
    name = "Projected State"
    def __init__(self, view, params):
        ViewColumn.__init__(self, view)
        self.columnText = ""
        self.size = 20
        self.fitImageId = view.imageList.Add(gui.bitmapLoader.getBitmap("fit_small", "icons"))
        self.moduleSlave = gui.builtinViewColumns.moduleState.ModuleState(view, params)
        self.droneSlave = gui.builtinViewColumns.droneCheckbox.DroneCheckbox(view, params)

    def getText(self, stuff):
        if isinstance(stuff, Module):
            return self.moduleSlave.getText(stuff)
        elif isinstance(stuff, Drone):
            return self.droneSlave.getText(stuff)
        else:
            return ""

    def getImageId(self, stuff):
        if isinstance(stuff, Module):
            return self.moduleSlave.getImageId(stuff)
        elif isinstance(stuff, Drone):
            return self.droneSlave.getImageId(stuff)
        else:
            return self.fitImageId

ProjectedState.register()
