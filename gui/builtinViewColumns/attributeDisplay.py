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
import controller
from util import shorten

class AttributeDisplay(ViewColumn):
    name = "Attribute Display"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        cAttribute = controller.Attribute.getInstance()
        info = cAttribute.getAttributeInfo(params["attribute"])
        self.info = info
        if params["showIcon"]:
            if info.name == "power":
                iconFile = "pg_small"
                iconType = "icons"
            else:
                iconFile = info.icon.iconFile if info.icon else None
                iconType = "pack"
            if iconFile:
                bitmap = bitmapLoader.getBitmap(iconFile, iconType)
                if bitmap:
                    self.imageId = fittingView.imageList.Add(bitmap)
                else:
                    self.imageId = -1
            else:
                self.imageId = -1
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name

    def getText(self, mod):
        attr = mod.getModifiedItemAttr(self.info.name)
        if attr:
            return (shorten(attr, 3, 0, 3))
        else:
            return ""

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return (("attribute", str, None),
                ("displayName", bool, False),
                ("showIcon", bool, True))

builtinViewColumns.registerColumn(AttributeDisplay)
