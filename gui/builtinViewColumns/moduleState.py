#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
from gui import bitmapLoader
from eos.types import State

class ModuleState(ViewColumn):
    name = "Module state"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 16
        self.stateNameMap = {}
        for state in State.__dict__:
            if state[0:2] == "__":
                continue

            id = State.__dict__[state]
            self.stateNameMap[id] = state.lower()

    def getText(self, mod):
        return ""

    def getImageId(self, mod):
        if mod.isEmpty():
            return -1
        else:
            bitmap = bitmapLoader.getBitmap("state_%s_small" % self.stateNameMap[mod.state], "icons")
            return self.fittingView.imageList.Add(bitmap)

builtinViewColumns.registerColumn(ModuleState)
