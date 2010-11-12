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

from gui.graph import Graph
import service
from gui import bitmapLoader
from eos.graph.fitDps import FitDpsGraph as FitDps
from eos.graph import Data
import gui.mainFrame
import service

class FitDpsGraph(Graph):
    propertyAttributeMap = {"transversal": "maxVelocity",
                            "distance": "maxRange",
                            "signatureRadius": "signatureRadius",
                            "velocity": "maxVelocity"}

    propertyLabelMap = {"transversal": "Transversal Speed:",
                        "distance": "Distance to Target:",
                        "signatureRadius": "Target Signature Radius:",
                        "velocity": "Target Velocity:"}

    def __init__(self):
        Graph.__init__(self)
        self.name = "DPS"
        self.fitDps = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getFields(self):
        return FitDps.defaults

    def getLabels(self):
        return self.propertyLabelMap

    def getIcons(self):
        icons = {}
        sFit = service.Attribute.getInstance()
        for key, attrName in self.propertyAttributeMap.iteritems():
            iconFile = sFit.getAttributeInfo(attrName).icon.iconFile
            bitmap = bitmapLoader.getBitmap(iconFile, "pack")
            if bitmap:
                icons[key] = bitmap

        return icons

    def getPoints(self, fit, fields):
        fitDps = getattr(self, "fitDps", None)
        if fitDps is None or fitDps.fit != fit:
            fitDps = self.fitDps = FitDps(fit)

        fitDps.clearData()
        variable = None
        for fieldName, value in fields.iteritems():
            d = Data(fieldName, value)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    #We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            fitDps.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in fitDps.getIterator():
            x.append(point[variable])
            y.append(val)

        return x, y

FitDpsGraph.register()
