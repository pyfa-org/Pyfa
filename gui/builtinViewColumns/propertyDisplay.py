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

from gui.viewColumn import ViewColumn
from gui.utils.numberFormatter import formatAmount
from service.attribute import Attribute


class PropertyDisplay(ViewColumn):
    name = "prop"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        sAttr = Attribute.getInstance()
        attributeSlave = params["attributeSlave"] or params["property"]
        # This function can throw an exception if the database isn't sane
        # We need to do a sanity check before this runs
        info = sAttr.getAttributeInfo(attributeSlave)

        self.mask = 0
        self.propertyName = params["property"]
        self.info = info
        if params["showIcon"]:
            if info.name == "power":
                iconFile = "pg_small"
                iconType = "gui"
            else:
                iconFile = info.iconID if info.icon else None
                iconType = "icons"
            if iconFile:
                self.imageId = fittingView.imageList.GetImageIndex(iconFile, iconType)
            else:
                self.imageId = -1
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name

    def getText(self, stuff):
        attr = getattr(stuff, self.propertyName, None)
        if attr:
            return formatAmount(attr, 3, 0, 3)
        else:
            return ""

    @staticmethod
    def getParameters():
        return (("property", str, None),
                ("attributeSlave", str, None),
                ("displayName", bool, False),
                ("showIcon", bool, True))


PropertyDisplay.register()
