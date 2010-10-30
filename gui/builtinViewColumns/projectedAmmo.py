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
import gui.builtinViewColumns.moduleAmmo
from eos.types import Module

class ProjectedAmmo(ViewColumn):
    name = "Projected Ammo"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.columnText = ""
        self.slave = gui.builtinViewColumns.moduleAmmo.ModuleAmmo(fittingView, params)
        self.imageId = self.slave.imageId
    def getText(self, stuff):
        if isinstance(stuff, Module):
            return self.slave.getText(stuff)
        else:
            return ""

    def getImageId(self, thing):
        if isinstance(thing, Module):
            return self.slave.getImageId(thing)
        else:
            return -1

ProjectedAmmo.register()
