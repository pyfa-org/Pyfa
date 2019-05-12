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
from eos.graph.fitCapTime import FitCapTimeGraph as EosFitCapTimeGraph
from gui.bitmap_loader import BitmapLoader
from gui.graph import Graph
from service.attribute import Attribute


class FitCapTimeGraph(Graph):

    propertyLabelMap = {"time": "Time (seconds)"}

    defaults = EosFitCapTimeGraph.defaults.copy()

    def __init__(self):
        Graph.__init__(self)
        self.defaults["time"] = "0-300"
        self.name = "Cap Amount vs. Time"
        self.fitCapTime = None
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
        fitCapTime = getattr(self, "fitCapTime", None)
        if fitCapTime is None or fitCapTime.fit != fit:
            fitCapTime = self.fitCapTime = EosFitCapTimeGraph(fit)

        fitCapTime.clearData()
        variable = None
        for fieldName, value in fields.items():
            d = Data(fieldName, value)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    # We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            fitCapTime.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in fitCapTime.getIterator():
            x.append(point[variable])
            y.append(val)
        return x, y


FitCapTimeGraph.register()
