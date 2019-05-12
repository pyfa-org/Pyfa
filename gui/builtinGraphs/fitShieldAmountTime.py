# =============================================================================
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
# =============================================================================

import gui.mainFrame
from eos.graph import Data
from eos.graph.fitShieldAmountTime import FitShieldAmountTimeGraph as EosFitShieldAmountTimeGraph
from gui.bitmap_loader import BitmapLoader
from gui.graph import Graph
from service.attribute import Attribute


class FitShieldAmountTimeGraph(Graph):

    propertyLabelMap = {"time": "Time (seconds)"}

    defaults = EosFitShieldAmountTimeGraph.defaults.copy()

    def __init__(self):
        Graph.__init__(self)
        self.defaults["time"] = "0-300"
        self.name = "Shield Amount vs Time"
        self.eosGraph = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getFields(self):
        return self.defaults

    def getLabels(self):
        return self.propertyLabelMap

    def getIcons(self):
        iconFile = Attribute.getInstance().getAttributeInfo('duration').iconID
        bitmap = BitmapLoader.getBitmap(iconFile, "icons")
        return {"time": bitmap}

    def getPoints(self, fit, fields):
        eosGraph = getattr(self, "eosGraph", None)
        if eosGraph is None or eosGraph.fit != fit:
            eosGraph = self.eosGraph = EosFitShieldAmountTimeGraph(fit)

        eosGraph.clearData()
        variable = None
        for fieldName, value in fields.items():
            d = Data(fieldName, value)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    # We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            eosGraph.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in eosGraph.getIterator():
            x.append(point[variable])
            y.append(val)
        return x, y

    @property
    def redrawOnEffectiveChange(self):
        return True


FitShieldAmountTimeGraph.register()
