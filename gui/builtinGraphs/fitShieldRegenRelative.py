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
from eos.graph.fitShieldRegenRelative import FitShieldRegenRelativeGraph as EosFitShieldRegenRelativeGraph
from gui.bitmap_loader import BitmapLoader
from gui.graph import Graph
from service.attribute import Attribute


class FitShieldRegenRelativeGraph(Graph):

    propertyLabelMap = {"percentage": "Shield Capacity (percent)"}

    defaults = EosFitShieldRegenRelativeGraph.defaults.copy()

    def __init__(self):
        Graph.__init__(self)
        self.defaults["percentage"] = "0-100"
        self.name = "Shield Regen vs. Shield Capacity"
        self.shieldRegenRelative = None
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getFields(self):
        return self.defaults

    def getLabels(self):
        return self.propertyLabelMap

    def getIcons(self):
        iconFile = Attribute.getInstance().getAttributeInfo('shieldCapacity').iconID
        bitmap = BitmapLoader.getBitmap(iconFile, "icons")
        return {"percentage": bitmap}

    def getPoints(self, fit, fields):
        shieldRegenRelative = getattr(self, "shieldRegenRelative", None)
        if shieldRegenRelative is None or shieldRegenRelative.fit != fit:
            shieldRegenRelative = self.shieldRegenRelative = EosFitShieldRegenRelativeGraph(fit)

        shieldRegenRelative.clearData()
        variable = None
        for fieldName, value in fields.items():
            d = Data(fieldName, value)
            if not d.isConstant():
                if variable is None:
                    variable = fieldName
                else:
                    # We can't handle more then one variable atm, OOPS FUCK OUT
                    return False, "Can only handle 1 variable"

            shieldRegenRelative.setData(d)

        if variable is None:
            return False, "No variable"

        x = []
        y = []
        for point, val in shieldRegenRelative.getIterator():
            x.append(point[variable])
            y.append(val)

        return x, y

    @property
    def redrawOnEffectiveChange(self):
        return True


FitShieldRegenRelativeGraph.register()
